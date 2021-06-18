<template>
  <nav class="w-screen h-12">
    <div
      class="w-screen h-full flex items-center px-4 bg-red-500"
      :class="{ 'justify-between': !!user, 'justify-center': !user }"
    >
      <router-link to="/" class="">
        <img class="h-12" src="../assets/logo.svg" alt="" />
      </router-link>

      <div v-if="user" class="flex space-x-2">
        <button @click="toggleSearchModal" class="nav-link">
          <img class="nav-icon" src="../assets/search.svg" alt="" />
        </button>
        <button @click="toggleGroupchatModal" class="nav-link">
          <img class="nav-icon" src="../assets/chat.svg" alt="" />
        </button>
        <router-link to="/settings" class="nav-link">
          <img class="nav-icon" src="../assets/settings.svg" alt="" />
        </router-link>
        <router-link v-if="user.role == 'admin'" to="/admin" class="nav-link">
          <img class="nav-icon" src="../assets/admin.svg" alt="" />
        </router-link>
      </div>
    </div>

    <SearchModal v-if="showSearchModal" @close="toggleSearchModal" />
    <GroupchatModal v-if="showGroupchatModal" @close="toggleGroupchatModal" />
  </nav>
</template>

<script>
import { ref, computed } from "vue";
import { useStore } from "vuex";
import SearchModal from "./SearchModal.vue";
import GroupchatModal from "./GroupchatModal.vue";
export default {
  components: {
    SearchModal,
    GroupchatModal,
  },
  setup() {
    const showSearchModal = ref(false);
    const showGroupchatModal = ref(false);

    const store = useStore();
    const user = computed(() => store.state.user);
    const isAdmin = user.value ? user.value.role == "admin" : false;

    const toggleSearchModal = function () {
      showSearchModal.value = !showSearchModal.value;
    };

    const toggleGroupchatModal = function () {
      showGroupchatModal.value = !showGroupchatModal.value;
    };

    return {
      isAdmin,
      user,
      showSearchModal,
      showGroupchatModal,
      toggleSearchModal,
      toggleGroupchatModal,
    };
  },
};
</script>
<style>
.nav-link {
  @apply w-9 h-9 flex items-center justify-center bg-black rounded-full bg-opacity-10 focus:outline-none;
}

.nav-icon {
  filter: brightness(0) saturate(100%);
  @apply w-5 h-5;
}
</style>