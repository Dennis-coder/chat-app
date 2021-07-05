<template>
  <modal :height="0.5">
    <div class="flex flex-col items-center space-y-2 h-full">
      <input
        type="text"
        class="input-field w-full rounded-md"
        placeholder="Search"
        v-model="term"
        v-debounce:300="search"
        ref="input"
      />
      <div
        v-if="results.length > 0"
        class="
          overflow-y-scroll
          w-full
          divide-y divide-gray-500
          bg-gray-70
          rounded-md
          py-1
          border border-gray-500
        "
      >
        <SearchResult
          v-for="result in results"
          :key="result.id"
          :result="result"
          @add="add"
          @accept="accept"
          @remove="remove"
          @deny="deny"
        />
      </div>
      <div v-else-if="term.length > 0" class="z-10 bg-gray-40 p-2">
        <p>No results</p>
      </div>
      <div
        v-else-if="requests && requests.length > 0"
        class="
          overflow-y-scroll
          w-full
          divide-y divide-gray-500
          bg-gray-70
          rounded-md
          py-1
          border border-gray-500
        "
      >
        <SearchResult
          v-for="request in requests"
          :key="request.id"
          :result="request"
          @add="add"
          @accept="accept"
          @remove="remove"
          @deny="deny"
        />
      </div>
    </div>
  </modal>
</template>

<script>
import axios from "axios";
import { computed, nextTick, ref } from "vue";
import { useStore } from "vuex";
import SearchResult from "./SearchResult.vue";
import Modal from "./Modal.vue";
export default {
  components: {
    SearchResult,
    modal: Modal,
  },
  setup() {
    const store = useStore();

    const requests = computed(() => store.state.requestsModule.requests);
    const socket = store.state.socket;

    const results = ref([]);
    const term = ref("");
    const input = ref(null);

    const search = async function () {
      if (term.value.length > 0) {
        results.value = (
          await axios.get("/api/v1/user/find", {
            params: { term: term.value },
          })
        ).data.filter((r) => r.id != store.state.user.id);
      } else {
        results.value = [];
      }
    };

    const add = async function (result) {
      await axios.post("/api/v1/friend/request", {
        friend_id: result.id,
      });
      store.dispatch("addPendingRequest", result);
      socket.emit("sentRequest", result.id);
    };

    const accept = async function (friendId) {
      let friend = (
        await axios.put("/api/v1/friend/request", {
          friend_id: friendId,
        })
      ).data;
      store.dispatch("addFriend", friend);
      store.dispatch("removeRequest", friendId);
      socket.emit("acceptedRequest", friendId);
    };

    const deny = async function (pending, friendId) {
      await axios.delete("/api/v1/friend/request", {
        data: { friend_id: friendId },
      });
      if (pending) {
        store.dispatch("removePendingRequest", friendId);
        socket.emit("withdrewRequest", friendId);
      } else {
        store.dispatch("removeRequest", friendId);
        socket.emit("deniedRequest", friendId);
      }
    };

    const remove = async function (friendId) {
      await axios.delete("/api/v1/friend", {
        data: { friend_id: friendId },
      });
      store.dispatch("removeFriend", friendId);
      socket.emit("removedFriend", friendId);
    };

    nextTick(() => {
      input.value.focus();
    });

    return {
      term,
      search,
      results,
      requests,
      add,
      accept,
      remove,
      deny,
      input,
    };
  },
};
</script>

<style>
</style>