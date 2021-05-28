<template>
  <div class="w-full flex items-center flex-col">
    <div>
      <button
        class="text-2xl w-36 py-2 hover:bg-gray-300 focus:outline-none"
        :class="{ 'bg-gray-200': tab === 0 }"
        @click="tab = 0"
      >
        Friends
      </button>
      <button
        class="text-2xl w-36 py-2 hover:bg-gray-300 focus:outline-none"
        :class="{ 'bg-gray-200': tab === 1 }"
        @click="tab = 1"
      >
        Groups
      </button>
    </div>
    <div v-if="tab === 0">
      <div>
        <input
          class="w-72 border border-gray-500 p-1"
          type="text"
          placeholder="Find a friend..."
          v-model="userSearch"
        />
      </div>
      <router-link
        v-for="friend in friendsFiltered"
        :key="friend.id"
        :to="`/friend/${friend.id}`"
        class="w-72 center-me flex-col p-2 hover:bg-gray-200"
      >
        <h2 class="text-2xl">{{ friend.username }}</h2>
        <p class="text-gray-400">{{ friend.lastInteraction }}</p>
      </router-link>
      <p
        v-if="friends.length > 0 && friendsFiltered.length === 0"
        class="text-center"
      >
        No friends matching
      </p>
      <div v-if="friends.length === 0" class="center-me flex-col">
        <p class="text-center">Try finding some friends to chat with</p>
        <router-link to="/find" class="text-center text-2xl">Click here to find a user</router-link>
      </div>
    </div>
    <div v-if="tab === 1">
      <div>
        <input
          class="w-72 border border-gray-500 p-1"
          type="text"
          placeholder="Find a group..."
          v-model="groupSearch"
        />
      </div>
      <a
        v-for="group in groupsFiltered"
        :key="group.id"
        href="#"
        class="w-72 center-me flex-col p-2 hover:bg-gray-200"
      >
        <h2 class="text-2xl">{{ group.name }}</h2>
        <p class="text-gray-400">{{ group.lastInteraction }}</p>
      </a>
      <p v-if="groups && groupsFiltered.length === 0" class="text-center">
        No groups matching
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      tab: 0,
      userSearch: "",
      groupSearch: "",
    };
  },
  async created() {
    this.$store.state.friends = (
      await axios.get(
        "/api/v1/friend/all?" + new URLSearchParams({ user_id: this.user.id })
      )
    ).data;
    this.$store.state.groups = (
      await axios.get(
        "/api/v1/group/all?" + new URLSearchParams({ user_id: this.user.id })
      )
    ).data;
  },
  computed: {
    user() {
      return this.$store.state.userModule.user;
    },

    friends() {
      return this.$store.state.friends;
    },

    friendsFiltered() {
      return this.friends.filter((friend) =>
        friend.username.includes(this.userSearch)
      );
    },

    groups() {
      return this.$store.state.groups;
    },

    groupsFiltered() {
      return this.groups.filter((group) =>
        group.name.includes(this.groupSearch)
      );
    },
  },
};
</script>

<style>
</style>