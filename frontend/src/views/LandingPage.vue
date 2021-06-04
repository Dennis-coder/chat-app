<template>
  <div class="h-full w-full flex items-center flex flex-col">
    <Navbar />
    <div class="center-me">
      <img class="" src="../assets/promo.jpg" alt="" />
      <h1 class="absolute text-white text-4xl text-center">
        The fastest way to share a moment!
      </h1>
    </div>

    <div class="fixed bottom-0 space-x-4 w-full center-me mb-4">
      <router-link to="/login" class="button1">Login</router-link>
      <router-link to="/register" class="button1">Register</router-link>
    </div>
  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue'
export default {
  components: {
    Navbar
  }
};
</script>