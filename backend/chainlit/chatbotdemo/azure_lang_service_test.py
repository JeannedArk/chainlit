#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from rich.tree import Tree
from rich import print
import azure_lang_service


QUESTIONS = [
    # "Aus welchen Teilen besteht der Geschäftsbericht?", # Eidgenössische Finanzmarktaufsicht FINMA Bundesgesetz über die Banken und Sparkassen YES
    # "Wie muss der Geschäftsbericht veröffentlicht werden?", # Eidgenössische Finanzmarktaufsicht FINMA Bundesgesetz über die Banken und Sparkassen YES
    "Was sind Auflagen zum Geschäftsbericht?", # Eidgenössische Finanzmarktaufsicht FINMA Bundesgesetz über die Banken und Sparkassen
    "Was sind die Anforderungen an systemrelevante Banken?", # Eidgenössische Finanzmarktaufsicht FINMA Bundesgesetz über die Banken und Sparkassen YES
    "Was sind die Anforderungen an Kantonalbanken?", # Eidgenössische Finanzmarktaufsicht FINMA Bundesgesetz über die Banken und Sparkassen YES

    "IKT-Strategie und Governance", # FINMA Operationelle Risiken und Resilienz

    "Wie sollen überfällige Zinsen behandelt werden?", # FINMA Rechnungslegungsvorschriften für Banken
]


def print_search_results(question: str, results: azure_lang_service.AzureSearchResponse) -> None:
    if not len(results.answers):
        print("[red]No results found")
        return

    print()
    tree = Tree(f"[blue]Question: {question}")
    for i, azure_search_answer in enumerate(results.answers):
        data_answ = tree.add(f"A{i}: {azure_search_answer.answer}")
        data_answ.add(f"[green]Confidence score: {azure_search_answer.confidence_score}")
        data_answ.add(f"[green]Source: {azure_search_answer.source}")

    print(tree)


def main(questions: List[str]):
    for question in questions:
        resp = azure_lang_service.search(question)
        print_search_results(question, resp)


if __name__ == '__main__':
    main(QUESTIONS)
