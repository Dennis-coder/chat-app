<template>
  <div class="py-1 px-2 flex justify-between items-center">
    <h2 class="text-lg">{{ result.username }}</h2>
    <button v-if="result.status === null" class="button3" @click="add">
      Add
    </button>
    <button
      v-else-if="result.status === 1 && result.sent_by === user.id"
      class="button3"
      @click="remove"
    >
      Sent
    </button>
    <div
      v-else-if="result.status === 1 && result.sent_by !== user.id"
      class="flex"
    >
      <button class="button3" @click="accept">Accept</button>
      <button class="button3" @click="remove">Remove</button>
    </div>
    <button v-else class="button3" @click="remove">Remove</button>
  </div>
</template>

<script>
import { useStore } from "vuex";
export default {
  props: {
    result: Object,
  },
  setup(props, { emit }) {
    const store = useStore();
    const user = store.state.user;

    const add = async function () {
      emit("add", props.result.id);
    };

    const accept = async function () {
      emit("accept", props.result.id);
    };

    const remove = async function () {
      emit("remove", props.result.id);
    };

    return { add, accept, remove, user };
  },
};
</script>

<style>
</style>