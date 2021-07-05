<template>
  <div class="flex flex-col h-full">
    <NavbarLite
      v-if="friend"
      :text="friend.username"
      @back="back"
      @toggleSettings="toggleSettings"
    />
    <div
      v-if="friend"
      class="
        max-w-sm
        w-full
        px-2
        space-y-2
        overflow-y-scroll
        pt-2
        pb-14
        mt-auto
      "
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
        class="
          absolute
          right-0
          w-9
          h-9
          center-me
          focus:outline-none
          rounded-full
          mr-2
          focus:bg-gray-400
        "
      >
        <img src="../assets/send.png" class="h-5" />
      </button>
    </form>
    <FriendSettingsModal
      v-if="showSettings"
      @close="toggleSettings"
      :friend="friend"
    />
  </div>
</template>

<script>
import axios from "axios";
import Message from "../components/Message.vue";
import NavbarLite from "../components/NavbarLite.vue";
import FriendSettingsModal from "../components/FriendSettingsModal.vue";
import { ref, nextTick, computed } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";

export default {
  components: {
    Message,
    NavbarLite,
    FriendSettingsModal,
  },
  setup() {
    const route = useRoute();
    const store = useStore();
    const router = useRouter();

    const messagesDiv = ref(null);
    const text = ref("");
    const messagesHeight = ref(0);
    const showSettings = ref(false);

    const user = store.state.user;
    const friend = computed(() =>
      store.state.friendsModule.friends.find(
        (friend) => friend.id === parseInt(route.params.id)
      )
    );
    const messages = computed(() =>
      friend.value ? friend.value.messages : []
    );
    const socket = store.state.socket;

    const sendMessage = async function () {
      let newMessage = (
        await axios.post("/api/v1/friend/message", {
          text: text.value,
          reciever_id: friend.value.id,
        })
      ).data;
      store.dispatch("addMessage", newMessage);
      socket.emit("chatMessage", newMessage);
      text.value = "";
      scrollDown();
    };

    const resizeEvent = function () {
      messagesHeight.value = window.innerHeight - 48;
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

    const toggleSettings = function () {
      showSettings.value = !showSettings.value;
    };

    const back = function () {
      router.push("/home");
    };

    window.addEventListener("resize", resizeEvent);
    nextTick(() => {
      resizeEvent();
      scrollDown();
    });

    return {
      friend,
      user,
      text,
      messagesHeight,
      messagesDiv,
      sendMessage,
      toggleSettings,
      showSettings,
      back,
      messages,
    };
  },
};
</script>

<style>
</style>