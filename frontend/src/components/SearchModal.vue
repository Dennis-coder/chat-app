<template>
  <div class="absolute top-0 w-screen h-screen center-me flex-col z-50">
    <input
      type="text"
      class="input-field w-3/4 z-10"
      placeholder="Search"
      v-model="term"
      v-debounce:300="search"
      ref="input"
    />
    <div
      v-if="results.length > 0"
      class="w-3/4 z-10 bg-gray-40 p-2 divide-y divide-gray-200"
    >
      <SearchResult
        v-for="result in results"
        :key="result.id"
        :result="result"
        @add="add"
        @accept="accept"
        @remove="remove"
      />
    </div>
    <div v-else-if="term.length > 0" class="w-3/4 z-10 bg-gray-40 p-2">
      <p>No results</p>
    </div>
    <div
      v-else-if="requests"
      class="w-3/4 z-10 bg-gray-40 p-2 divide-y divide-gray-200"
    >
      <SearchResult
        v-for="request in requests"
        :key="request.id"
        :result="request"
        @add="add"
        @accept="accept"
        @remove="remove"
      />
    </div>
    <div
      class="absolute top-0 w-screen h-screen bg-black bg-opacity-70"
      @click="close"
    ></div>
  </div>
</template>

<script>
import axios from "axios";
import { nextTick, ref } from "vue";
import { useStore } from "vuex";
import SearchResult from "./SearchResult.vue";
export default {
  components: {
    SearchResult,
  },
  setup(_, { emit }) {
    const results = ref([]);
    const term = ref("");
    const store = useStore();
    const user = store.state.user;
    const requests = ref(null);
    const input = ref(null);

    const close = function () {
      emit("close");
    };

    const search = async function () {
      if (term.value.length > 0) {
        results.value = (
          await axios.get("/api/v1/user/find", {
            params: { term: term.value, user_id: user.id },
          })
        ).data;
        console.log(results.value);
      } else {
        results.value = [];
      }
    };

    const add = async function (friend_id) {
      await axios.post("/api/v1/friend", {
        user_id: user.id,
        friend_id,
      });
      let result = results.value.find((result) => result.id === friend_id);
      result.status = 1;
      result.sent_by = user.id;
    };

    const accept = async function (friend_id) {
      let friend = (await axios.put("/api/v1/friend", {
        user_id: user.id,
        friend_id,
      })).data
			store.dispatch('addFriend', friend)

      friend = requests.value.find((request) => request.id === friend_id);
			if (!friend) {
				friend = results.value.find((result) => result.id === friend_id);
			}
			friend.status = 0;
    };

    const remove = async function (friend_id) {
      await axios.delete("/api/v1/friend", {
        data: { user_id: user.id, friend_id },
      });
			store.dispatch('removeFriend', friend_id)
      let result = results.value.find((result) => result.id === friend_id);
      result.status = null;
      result.sent_by = null;
    };

    const fetchRequests = async function () {
      requests.value = (
        await axios.get("/api/v1/friend/requests", {
          params: { user_id: user.id },
        })
      ).data;
    };

    fetchRequests();

    nextTick(() => {
      input.value.focus();
    });

    return { term, close, search, results, requests, add, accept, remove, input };
  },
};
</script>

<style>
</style>