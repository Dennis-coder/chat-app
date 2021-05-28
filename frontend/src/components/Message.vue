<template>
  <div class="w-max" style="max-width: 16rem">
    <div @click="toggleTimestamp" class="rounded-2xl py-1 px-2 w-max max-w-full">
      <p class="w-max break-words max-w-full">{{ message.text }}</p>
    </div>
    <p v-if="showTimestamp" class="w-max text-xs">{{ timestamp }}</p>
  </div>
</template>

<script>
export default {
  props: {
    message: Object
  },
  data() {
    return {
      showTimestamp: false,
    }
  },
  computed: {
    timestamp() {
      return this.message.timestamp.substring(0, 5)
    }
  },
  methods: {
    toggleTimestamp() {
      this.showTimestamp = !this.showTimestamp
    }
  }
};
</script>

<style>
</style>