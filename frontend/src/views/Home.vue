<template>
  <div class="w-full flex items-center flex-col">
    <div class="w-full flex flex-col items-center bg-gray-70">
      <div class="w-full">
        <button
          class="tab-button"
          :class="{ 'bg-gray-40': tab !== 0 }"
          @click="tab = 0"
        >
          Friends
        </button>
        <button
          class="tab-button"
          :class="{ 'bg-gray-40': tab !== 1 }"
          @click="tab = 1"
        >
          Groups
        </button>
      </div>
      <input
        class="input-field w-3/4 rounded-full my-2"
        type="text"
        :placeholder="`Find a ${tab == 0 ? 'friend' : 'group'}`"
        v-model="searchTerm"
      />
    </div>
    <div
      v-show="tab === 0"
      class="tab"
      :style="{ 'max-height': height + 'px' }"
    >
      <router-link
        v-for="friend in friendsFiltered"
        :key="friend.id"
        :to="`/friend/${friend.id}`"
        class="link"
      >
        <h2 class="name">{{ friend.username }}</h2>
        <p class="timestamp">{{ friend.lastInteraction }}</p>
      </router-link>
      <p
        v-if="friends.length > 0 && friendsFiltered.length === 0"
        class="no-match"
      >
        No friends matching
      </p>
      <div v-if="friends.length === 0" class="new-user">
        <p>Try finding some friends to chat with</p>
        <button class="text-2xl">Click here to find a user</button>
      </div>
    </div>
    <div
      v-show="tab === 1"
      class="tab"
      :style="{ 'max-height': height + 'px' }"
    >
      <router-link
        v-for="group in groupsFiltered"
        :key="group.id"
        :to="`/group/${group.id}`"
        class="link"
      >
        <h2 class="name">{{ group.name }}</h2>
        <p class="timestamp">{{ group.lastInteraction }}</p>
      </router-link>
      <p
        v-if="groups.length > 0 && groupsFiltered.length === 0"
        class="no-match"
      >
        No groups matching
      </p>
      <div v-if="groups.length === 0" class="new-user">
        <p>You are not in a group yet</p>
        <button class="text-2xl">Click here to create a group</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, computed, nextTick } from "vue";
import { useStore } from "vuex";

export default {
  setup() {
    const tab = ref(0);
    const height = ref(0);
    const searchTerm = ref("");
    const store = useStore();
    const user = store.state.user;
    const friends = computed(() => store.state.friends);
    const groups = computed(() => store.state.groups);

    const friendsFiltered = computed(() =>
      friends.value.filter((friend) =>
        friend.username.includes(searchTerm.value)
      )
    );

    const groupsFiltered = computed(() =>
      groups.value.filter((group) => group.name.includes(searchTerm.value))
    );

    const loadData = async function () {
      store.dispatch(
        "setFriends",
        (
          await axios.get("/api/v1/friend/all", {
            params: { user_id: user.id },
          })
        ).data
      );
      store.dispatch(
        "setGroups",
        (await axios.get("/api/v1/group/all", { params: { user_id: user.id } }))
          .data
      );
    };

    const resizeEvent = function () {
      height.value = window.innerHeight - 144;
    };

    loadData();
    window.addEventListener("resize", resizeEvent);
    nextTick(() => {
      resizeEvent();
    });

    return {
      tab,
      searchTerm,
      friends,
      groups,
      friendsFiltered,
      groupsFiltered,
      height,
    };
  },
};
</script>

<style>
.name {
  @apply text-2xl;
}
.timestamp {
  @apply text-gray-400;
}
.no-match {
  @apply text-gray-400 text-center mt-2 text-lg;
}
.link {
  @apply w-full flex items-center flex-col p-2 hover:bg-gray-200;
}
.tab {
  @apply w-full divide-y divide-gray-400 overflow-y-scroll;
}
.tab-button {
  @apply text-2xl w-1/2 py-2 focus:outline-none;
}
.new-user {
  @apply flex items-center flex-col mt-2;
}
</style>