<template>
  <div class="flex flex-col h-full">
    <div class="w-full h-10 bg-gray-70 bg-opacity-80 center-me">
      <h2 v-if="group" class="text-2xl">{{ group.name }}</h2>
    </div>
    <div
      v-if="messages && !loadingMessages"
      class="max-w-sm w-full px-2 space-y-2 overflow-y-scroll pt-2 pb-14 mt-auto"
      :style="{ 'max-height': messagesHeight + 'px' }"
      ref="messagesDiv"
    >
      <Message
        v-for="message in messages"
        :key="message.id"
        :message="message"
        :class="{
          'your-message': message.senderId === user.id,
          'others-message': message.senderId !== user.id,
        }"
      />
    </div>
    <form
      class="fixed bottom-0 w-full h-12 flex bg-gray-70 bg-opacity-80 center-me"
    >
      <input
        type="text"
        placeholder="Send a message"
        class="input-field w-full rounded-full m-2 mr-14"
        v-model="text"
      />
      <button
        :disabled="text.length === 0"
        @click.prevent="sendMessage"
        class="absolute right-0 w-9 h-9 center-me focus:outline-none rounded-full mr-2 focus:bg-gray-400"
      >
        <img src="../assets/send.png" class="h-5" />
      </button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import Message from "../components/Message.vue";
import { ref, nextTick, onUnmounted } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";

export default {
  components: {
    Message,
  },
  setup() {
    const group = ref(null);
    const friends = ref(null);
    const messages = ref(null);
    const messagesDiv = ref(null);

    const text = ref("");
    const messagesHeight = ref(0);
    const loadingMessages = ref(true);

    const route = useRoute();
    const store = useStore();
    const user = ref(store.state.user);
    const socket = store.state.socket;

    socket.emit("join-group", route.params.id);

    socket.on(`group message`, (newMessage) => {
      messages.value.push(newMessage);
      scrollDown();
    });

    const loadData = async function () {
      if (store.state.groups.length > 0) {
        group.value = store.state.groups.find(
          (group) => (group.id = route.params.id)
        );
      } else {
        group.value = (
          await axios.get("/api/v1/group", {
            params: { group_id: route.params.id },
          })
        ).data;
      }

      messages.value = (
        await axios.get("/api/v1/group/messages", {
          params: { group_id: route.params.id },
        })
      ).data;

      friends.value = (
        await axios.get("/api/v1/group/members", {
          params: { group_id: route.params.id },
        })
      ).data;

      loadingMessages.value = false;
    };

    const sendMessage = async function () {
      let newMessage = (
        await axios.post("/api/v1/group/message", {
          text: text.value,
          sender_id: user.value.id,
          group_id: group.value.id,
        })
      ).data;
      messages.value.push(newMessage);
      socket.emit(`group message`, newMessage);
      text.value = "";
      scrollDown();
    };

    const resizeEvent = function () {
      messagesHeight.value = window.innerHeight - 88;
    };

    const scrollDown = async function () {
      nextTick(async () => {
        if (messagesDiv.value) {
          messagesDiv.value.scrollTop = messagesDiv.value.scrollHeight;
        } else {
          await new Promise((r) => setTimeout(r, 50));
          scrollDown();
        }
      });
    };

    loadData();
    window.addEventListener("resize", resizeEvent);
    nextTick(() => {
      resizeEvent();
      scrollDown();
    });

    onUnmounted(() => {
      socket.emit("leave-group", group.value.id);
    });

    return {
      group,
      friends,
      user,
      messages,
      text,
      messagesHeight,
      loadingMessages,
      socket,
      messagesDiv,
      sendMessage,
    };
  },
};
</script>

<style>
</style>