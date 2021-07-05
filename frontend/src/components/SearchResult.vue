<template>
  <div class="py-1 px-2 flex justify-between items-center">
    <h2 class="text-lg">{{ result.username }}</h2>
    <button v-if="isFriend" class="button3" @click="remove">Remove</button>
    <div v-else-if="requestPending" class="flex">
      <button class="button3" @click="accept">Accept</button>
      <button class="button3" @click="deny(false)">Decline</button>
    </div>
    <button v-else-if="requestSent" class="button3" @click="deny(true)">
      Sent
    </button>
    <button v-else class="button3" @click="add">Add</button>
  </div>
</template>

<script>
import { computed } from "@vue/runtime-core";
import { useStore } from "vuex";
export default {
  props: {
    result: Object,
  },
  setup(props, { emit }) {
    const store = useStore();
    const user = store.state.user;

    const isFriend = computed(
      () =>
        !!store.state.friendsModule.friends.find(
          (f) => f.id === props.result.id
        )
    );
    const requestPending = computed(
      () =>
        !!store.state.requestsModule.requests.find(
          (r) => r.id === props.result.id
        )
    );
    const requestSent = computed(
      () =>
        !!store.state.requestsModule.pendingRequests.find(
          (r) => r.id === props.result.id
        )
    );

    const add = async function () {
      emit("add", props.result);
    };

    const accept = async function () {
      emit("accept", props.result.id);
    };

    const remove = async function () {
      emit("remove", props.result.id);
    };

    const deny = async function (pending) {
      emit("deny", pending, props.result.id);
    };

    return {
      add,
      accept,
      remove,
      deny,
      user,
      isFriend,
      requestPending,
      requestSent,
    };
  },
};
</script>

<style>
</style>