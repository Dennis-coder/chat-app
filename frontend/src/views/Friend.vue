<template>
  <div class="center-me flex-col mt-auto">
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
      class="fixed bottom-0 w-full h-12 flex bg-gray-400 bg-opacity-90 center-me"
    >
      <input
        type="text"
        placeholder="Send a message"
        class="w-full rounded-3xl p-3 m-2 mr-14 focus:outline-none h-8"
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
import { ref, nextTick } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'

export default {
  components: {
    Message,
  },
  setup() {
    const friend = ref(null)
    const messages = ref(null)
    const messagesDiv = ref(null)
    
    const text = ref('')
    const messagesHeight = ref(0)
    const loadingMessages = ref(true)

    const route = useRoute()
    const store = useStore()
    const user = ref(store.state.userModule.user)
    const socket = ref(store.state.socket)


    const loadData = async function() {
      if (store.state.friends.length > 0) {
        friend.value = store.state.friends.find(
          (friend) => (friend.id = route.params.id)
        );
      } else {
        friend.value = (
          await axios.get(
            "/api/v1/friend?" +
              new URLSearchParams({
                friend_id: route.params.id,
                user_id: user.value.id,
              })
          )
        ).data;
      }
      messages.value = (
        await axios.get(
          "/api/v1/message/all?" +
            new URLSearchParams({
              friend_id: route.params.id,
              user_id: user.value.id,
            })
        )
      ).data;
  
      loadingMessages.value = false
    }

    const sendMessage = async function() {
      let newMessage = (
        await axios.post("/api/v1/message", {
          text: text.value,
          sender_id: user.value.id,
          reciever_id: friend.value.id,
        })
      ).data;
      messages.value.push(newMessage);
      store.dispatch('emitSocketEvent', { event: "chat message", args: { event: `user-${friend.value.id}`, data: newMessage } })
      text.value = "";
      scrollDown()
    }

    const resizeEvent = function() {
      messagesHeight.value = window.innerHeight - 48;
    }

    const scrollDown = async function() {
      nextTick(async () => {
        if (messagesDiv.value) {
        messagesDiv.value.scrollTop = messagesDiv.value.scrollHeight;
      } else {
        await new Promise((r) => setTimeout(r, 50));
        scrollDown();
      }
      })
    }

    window.addEventListener("resize", resizeEvent);
    loadData()
    nextTick(() => {
      resizeEvent();
      scrollDown();
    });

    return {friend, user, messages, text, messagesHeight, loadingMessages, socket, messagesDiv, sendMessage}
  },
};
</script>

<style>
</style>