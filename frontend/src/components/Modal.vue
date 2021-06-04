<template>
  <div class="absolute top-0 w-screen h-screen center-me flex-col z-50">
    <div
      class="z-50 w-3/4 bg-gray-40 rounded-lg p-2 relative"
      :style="{ maxHeight: `${maxHeight}px` }"
    >
      <button class="absolute top-0 right-0 nav-link m-1" @click="close">
        <img src="../assets/x.svg" class="nav-icon">
      </button>
      <slot></slot>
    </div>
    <div
      class="absolute top-0 w-screen h-screen bg-black bg-opacity-70"
      @click="close"
    ></div>
  </div>
</template>

<script>
import { ref, nextTick } from 'vue'
export default {
  props: {
    height: Number
  },
  setup(props, { emit }) {
    const maxHeight = ref(0);

    const close = function () {
      emit("close");
    };

    const resizeEvent = function () {
      maxHeight.value = window.innerHeight * props.height;
    };

    window.addEventListener("resize", resizeEvent);
    nextTick(() => {
      resizeEvent();
    });

    return { close, maxHeight };
  },
};
</script>

<style>
</style>