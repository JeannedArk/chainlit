import { IConversation, IPrompt } from '@chainlit/components';

import {
  IPageInfo,
  IPagination
} from 'components/organisms/conversationsHistory/sidebar/ConversationsHistoryList';

import { IConversationsFilters } from 'state/conversations';

import { api } from '.';

const ChainlitAPI = {
  getCompletion: async (
    prompt: IPrompt,
    userEnv = {},
    controller: AbortController,
    accessToken?: string,
    tokenCb?: (done: boolean, token: string) => void
  ) => {
    const response = await api.post(
      `/completion`,
      { prompt, userEnv },
      accessToken,
      controller.signal
    );

    const reader = response?.body?.getReader();

    const stream = new ReadableStream({
      start(controller) {
        function push() {
          reader!
            .read()
            .then(({ done, value }) => {
              if (done) {
                controller.close();
                tokenCb && tokenCb(done, '');
                return;
              }
              const string = new TextDecoder('utf-8').decode(value);
              tokenCb && tokenCb(done, string);
              controller.enqueue(value);
              push();
            })
            .catch((err) => {
              controller.close();
              tokenCb && tokenCb(true, '');
              console.error(err);
            });
        }
        push();
      }
    });

    return stream;
  },

  setHumanFeedback: async (
    messageId: string,
    feedback: number,
    feedbackComment?: string,
    accessToken?: string
  ) => {
    await api.put(
      `/message/feedback`,
      { messageId, feedback, feedbackComment },
      accessToken
    );
  },

  getConversations: async (
    pagination: IPagination,
    filter: IConversationsFilters,
    accessToken?: string
  ): Promise<{
    pageInfo: IPageInfo;
    data: IConversation[];
  }> => {
    const res = await api.post(
      `/project/conversations`,
      { pagination, filter },
      accessToken
    );

    return res?.json();
  },

  deleteConversation: async (conversationId: string, accessToken?: string) => {
    const res = await api.delete(
      `/project/conversation`,
      { conversationId },
      accessToken
    );

    return res?.json();
  }
};

export { ChainlitAPI };
