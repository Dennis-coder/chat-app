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

export default {
  components: {
    Message,
  },
  data() {
    return {
      friendData: null,
      messages: null,
      text: "",
      messagesHeight: 0,
      loadingMessages: true
    };
  },
  async created() {
    if (this.$store.state.friends.length > 0) {
      this.friendData = this.$store.state.friends.find(
        (friend) => (friend.id = this.$route.params.id)
      );
    } else {
      this.friendData = (
        await axios.get(
          "/api/v1/friend?" +
            new URLSearchParams({
              friend_id: this.$route.params.id,
              user_id: this.user.id,
            })
        )
      ).data;
    }
    this.messages = (
      await axios.get(
        "/api/v1/message/all?" +
          new URLSearchParams({
            friend_id: this.$route.params.id,
            user_id: this.user.id,
          })
      )
    ).data;
    this.loadingMessages = false
    this.socket.on(`user-${this.user.id}`, function(newMessage) {
      console.log(user)
      this.messages.push(newMessage)
    });
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener("resize", this.resizeEvent);
      this.resizeEvent();
      this.scrollDown();
    });
  },
  computed: {
    user() {
      return this.$store.state.userModule.user;
    },

    friend() {
      return this.friendData ? this.friendData : null;
    },

    socket() {
      return this.$store.state.socket;
    }
  },
  methods: {
    async sendMessage() {
      let newMessage = (
        await axios.post("/api/v1/message", {
          text: this.text,
          sender_id: this.user.id,
          reciever_id: this.friend.id,
        })
      ).data;
      this.messages.push(newMessage);
      this.$store.dispatch('emitSocketEvent', { event: "chat message", args: { event: `user-${this.friend.id}`, message: newMessage } })
      this.text = "";
      this.scrollDown()
    },

    resizeEvent() {
      this.messagesHeight = window.innerHeight - 48;
    },
    async scrollDown() {
      this.$nextTick(async () => {
        if (this.$refs.messagesDiv) {
        this.$refs.messagesDiv.scrollTop = this.$refs.messagesDiv.scrollHeight;
      } else {
        await new Promise((r) => setTimeout(r, 50));
        this.scrollDown();
      }
      })
    },
  },
};
</script>

<style>
</style>