<template>
  <div class="absolute top-0 w-screen h-screen center-me flex-col z-50">
    <div
      class="absolute top-0 w-screen h-screen bg-black bg-opacity-70"
      @click="close"
    ></div>
  </div>
</template>

<script>
// import axios from "axios";
// import { ref } from "vue";
import { useStore } from "vuex";
export default {
  setup(_, { emit }) {
    const store = useStore();
    const user = store.state.user;

    const close = function () {
      emit("close");
    };

    return { user, close };
  },
};
</script>

<style>
</style>