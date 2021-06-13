<template>
  <modal :height="0.5">
    <div class="flex flex-col items-center space-y-2 h-full">
      <h2 class="text-2xl">Create a group</h2>
      <input
        class="input-field w-full rounded-md"
        type="text"
        v-model="name"
        placeholder="Name of group"
      />
      <input
        class="input-field w-full rounded-md"
        type="text"
        v-model="filter"
        placeholder="Search"
      />
      <div
        class="
          overflow-y-scroll
          w-full
          divide-y divide-gray-500
          bg-gray-70
          rounded-md
          border border-gray-500
        "
      >
        <div
          v-for="friend in friendsFiltered"
          :key="friend.id"
          class="py-1 px-2 flex items-center"
          @click="toggleSelected(friend.id)"
        >
          <img
            v-if="selectedIds.includes(friend.id)"
            src="../assets/checkmark.png"
            class="checkmark h-4 mr-1"
          />
          <h2 class="text-xl">{{ friend.username }}</h2>
        </div>
      </div>
      <button @click="createGroup" :disabled="disableButton" class="button2">
        Create
      </button>
    </div>
  </modal>
</template>

<script>
import axios from "axios";
import { computed, ref } from "vue";
import { useStore } from "vuex";
import Modal from "./Modal.vue";
export default {
  components: {
    modal: Modal,
  },
  setup() {
    const store = useStore();
    const user = store.state.user;
    const friends = store.state.friends;
    const selectedIds = ref([]);

    const name = ref("");
    const filter = ref("");

    const disableButton = computed(
      () => name.value.length === 0 || selectedIds.value.length < 2
    );

    const friendsFiltered = computed(() =>
      friends.filter((friend) =>
        friend.username.toLowerCase().includes(filter.value)
      )
    );

    const toggleSelected = function (id) {
      if (selectedIds.value.includes(id)) {
        let index = selectedIds.value.indexOf(id);
        selectedIds.value.splice(index, 1);
      } else {
        selectedIds.value.push(id);
      }
    };

    const createGroup = async function () {
      let group = (
        await axios.post("/api/v1/group", {
          name: name.value,
          users: selectedIds.value,
        })
      ).data;
      store.dispatch("addGroup", group);
      close();
    };

    return {
      user,
      name,
      selectedIds,
      toggleSelected,
      createGroup,
      disableButton,
      friendsFiltered,
      filter,
    };
  },
};
</script>

<style>
.checkmark {
  filter: invert(38%) sepia(61%) saturate(3925%) hue-rotate(338deg)
    brightness(97%) contrast(92%);
}
</style>