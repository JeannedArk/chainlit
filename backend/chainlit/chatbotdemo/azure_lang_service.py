# -*- coding: utf-8 -*-
import os
from dataclasses import dataclass
from typing import List
import requests


ENV_NAME_OCP_APIM_SUBSCRIPTION_KEY = "ENV_OCP_APIM_SUBSCRIPTION_KEY"

COGNITIVE_SEARCH_ENDPOINT = "https://ai-demo-2-timo-language-service.cognitiveservices.azure.com/language/:query-knowledgebases?projectName=AKBBankingComplianceDemo&api-version=2021-10-01&deploymentName=production"
NUM_ANSWERS = 2
CONFIDENCE_SCORE_THRESHOLD = 0.4

PDF_NAME_TITLE_MAPPING = {
    "Eidgenössische Finanzmarktaufsicht FINMA Bundesgesetz über die Banken und Sparkassen.pdf": "Bundesgesetz über die Banken und Sparkassen",
}


@dataclass(frozen=True)
class AzureSearchAnswer:
    answer: str
    confidence_score: float
    id: str
    source: str

    @staticmethod
    def from_json(o):
        source = PDF_NAME_TITLE_MAPPING[o["source"]] if "source" in o and o["source"] in PDF_NAME_TITLE_MAPPING else None
        return AzureSearchAnswer(
            answer=o["answer"],
            confidence_score=o["confidenceScore"],
            id=o["id"],
            source=source,
        )


@dataclass(frozen=True)
class AzureSearchResponse:
    answers: List[AzureSearchAnswer]

    @staticmethod
    def from_json(o):
        if "error" in o:
            return AzureSearchResponse(answers=[])
        answers = [AzureSearchAnswer.from_json(answer) for answer in o["answers"]]
        # Filter answers without answer text
        answers_filtered = [a for a in answers if a.answer and a.answer.lower() != "no answer found"]
        return AzureSearchResponse(answers=answers_filtered)


def get_env_var(var_name: str):
    try:
        return os.environ[var_name]
    except KeyError as e:
        print(f"Environment variable {var_name} not set")
        raise e


def search(question) -> AzureSearchResponse:
    """
    A request can look like this:
    "{\"top\":3,\"question\":\"YOUR_QUESTION_HERE\"," \
    "\"includeUnstructuredSources\":true," \
    "\"confidenceScoreThreshold\":\"YOUR_SCORE_THRESHOLD_HERE\"," \
    "\"answerSpanRequest\":{\"enable\":true,\"topAnswersWithSpan\":1,\"confidenceScoreThreshold\":\"YOUR_SCORE_THRESHOLD_HERE\"},\"filters\":{\"metadataFilter\":{\"logicalOperation\":\"YOUR_LOGICAL_OPERATION_HERE\",\"metadata\":[{\"key\":\"YOUR_ADDITIONAL_PROP_KEY_HERE\",\"value\":\"YOUR_ADDITIONAL_PROP_VALUE_HERE\"}]}}}"
    """
    body = {
        "top": NUM_ANSWERS,
        "question": question,
        "includeUnstructuredSources": True,
        "confidenceScoreThreshold": CONFIDENCE_SCORE_THRESHOLD,
    }
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": get_env_var(ENV_NAME_OCP_APIM_SUBSCRIPTION_KEY),
    }
    resp = requests.post(COGNITIVE_SEARCH_ENDPOINT, json=body, headers=headers)
    resp_json = resp.json()
    return AzureSearchResponse.from_json(resp_json)
