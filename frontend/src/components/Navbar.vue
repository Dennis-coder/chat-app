<template>
  <nav class="w-screen h-12 relative">
    <div
      class="z-20 w-screen h-full flex items-center justify-center px-8 relative bg-red-500"
    >
      <router-link v-if="user" to="/find" class="w-8 h-8 center-me bg-black rounded-full bg-opacity-20">
        <img class="w-5 h-5" src="../assets/search.svg" alt="" />
      </router-link>
      <router-link to="/" class="m-auto">
        <img class="w-8 h-8" src="../assets/logo.png" alt="" />
      </router-link>
      <router-link v-if="user" to="/settings" class="w-8 h-8 center-me bg-black rounded-full bg-opacity-20">
        <img class="w-5 h-5" src="../assets/settings.svg" alt="" />
      </router-link>

    </div>
  </nav>
</template>

<script>
import { useStore } from 'vuex'
export default {
  setup() {
    const store = useStore()
    const user = store.state.userModule.user
    const isAdmin = user ? user.role == "admin" : false;

    return {isAdmin, user}
  },
};
</script>