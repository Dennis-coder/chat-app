<template>
  <div class="w-max" style="max-width: 16rem">
    <div
      @click="toggleTimestamp"
      class="rounded-2xl py-1 px-2 w-max max-w-full"
    >
      <p class="w-max break-words max-w-full">{{ message.text }}</p>
    </div>
    <p v-if="showTimestamp" class="w-max text-xs">{{ timestamp }}</p>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  props: {
    message: Object,
  },
  setup(props) {
    const showTimestamp = ref(false);
    const timestamp = props.message.timestamp.substring(0, 5);

    const toggleTimestamp = function () {
      showTimestamp.value = !showTimestamp.value;
    };

    return {
      showTimestamp,
      timestamp,
      toggleTimestamp,
    };
  },
};
</script>

<style>
</style>