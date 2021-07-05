<template>
  <modal :height="0.5">
    <div class="flex flex-col items-center space-y-2">
      <h2 class="text-2xl">Settings</h2>
      <button class="button3" @click="remove">Remove friend</button>
    </div>
  </modal>
</template>

<script>
import axios from "axios";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import Modal from "./Modal.vue";
export default {
  components: {
    modal: Modal,
  },
  props: {
    friend: Object,
  },
  setup(props) {
    const store = useStore();
    const router = useRouter();

    const socket = store.state.socket;

    const remove = async function () {
      try {
        await axios.delete("/api/v1/friend", {
          data: { friend_id: props.friend.id },
        });
        store.dispatch("removeFriend", props.friend.id);
        socket.emit("removedFriend", props.friend.id);
        router.push("/home");
      } catch (error) {
        console.error(error);
      }
    };

    return { remove };
  },
};
</script>

<style>
</style>