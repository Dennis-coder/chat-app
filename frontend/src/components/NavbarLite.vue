<template>
  <div class="w-full h-12 bg-red-500 px-2 center-me relative">
    <button
      class="nav-link transform rotate-180 absolute left-0 ml-2"
      @click="back"
    >
      <img src="../assets/arrow.svg" class="nav-icon" />
    </button>
    <h2 class="text-2xl text-black">{{ text }}</h2>
    <button
      v-if="settings"
      class="nav-link absolute right-0 mr-2"
      @click="toggleSettings"
    >
      <img src="../assets/settings.svg" class="nav-icon" />
    </button>
  </div>
</template>

<script>
export default {
  props: {
    text: String,
    settings: {
      type: Boolean,
      default: true,
    },
  },
  setup(_, { emit }) {
    const back = function () {
      emit("back");
    };
    const toggleSettings = function () {
      emit("toggleSettings");
    };
    return { back, toggleSettings };
  },
};
</script>

<style>
</style>