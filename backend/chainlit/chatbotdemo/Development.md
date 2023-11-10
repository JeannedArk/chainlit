## Azure Setup

https://language.cognitive.azure.com/questionAnswering/projects/pilatus-test-project2/deploy


## Resources

* Azure Cognitive Search:
  * Create the service: https://learn.microsoft.com/en-us/azure/search/search-create-service-portal
  * Set up language studio: https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/language-studio
    * In the language studio UI in the `Select Azure resource` popup click `Create a new Language resource in the Azure portal` to create a Language Service.
    * Click `Select` to enable `Custom question answering`.
    * When the created resource is not available in the language studio, then purge the cache and cookies.
    * Click `Create new`, select `Custom question answering`.
    * Select English as language and create the project.
    * In `Manage sources` click `Add source` and select `Files`.
    * Add the documents from the `documents/pc24` folder. Name them and select `Auto-detect` ?
    * In `Deploy knowledge base` click `Deploy` to deploy the knowledge base.
    * Click `Get Prediction URL`. Use the URL as endpoint. Use the `Ocp-Apim-Subscription-Key` in `Sample request` as key.
  * Creating chat bot, language resource key: https://stackoverflow.com/questions/75262088/azure-bot-giving-error-in-web-test-chat-to-continue-to-run-this-bot-please-fix

## Literature:
* https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/overview
* Models: https://learn.microsoft.com/en-au/azure/cognitive-services/openai/concepts/models