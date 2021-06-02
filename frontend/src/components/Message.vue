<template>
  <div class="w-max flex items-center">
    <p v-if="showTimestamp" class="timestamp w-max text-xs">{{ timestamp }}</p>
    <div
      @click="toggleTimestamp"
      class="rounded-2xl py-1 px-2 w-max max-w-full"
      style="max-width: 16rem"
    >
      <p class="w-max break-words max-w-full">{{ message.text }}</p>
    </div>
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
.your-message {
  @apply ml-auto flex-row-reverse;
}

.your-message div {
  @apply bg-blue-600 text-white;
}

.your-message .timestamp {
  @apply ml-1;
}

.others-message div {
  @apply bg-gray-200 text-black;
}

.others-message .timestamp {
  @apply mr-1;
}
</style>