<template>
  <modal :height="0.7">
    <div class="flex flex-col items-center space-y-2 h-full overflow-y-scroll">
      <h2 class="text-2xl">Settings</h2>
      <div
        class="w-full flex flex-col items-center overflow-y-hidden space-y-1"
      >
        <p>Members</p>
        <input
          class="input-field w-full rounded-md"
          type="text"
          v-model="membersFilter"
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
            v-for="member in membersFiltered"
            :key="member.id"
            class="py-1 px-2 flex items-center justify-between"
          >
            <h2 class="text-xl">{{ member.username }}</h2>
            <button v-if="isOwner" class="button3" @click="remove(member.id)">
              Remove
            </button>
          </div>
        </div>
      </div>
      <div
        class="w-full flex flex-col items-center overflow-y-hidden space-y-1"
      >
        <p>Friends</p>
        <input
          class="input-field w-full rounded-md"
          type="text"
          v-model="friendsFilter"
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
            class="py-1 px-2 flex items-center justify-between"
          >
            <h2 class="text-xl">{{ friend.username }}</h2>
            <button class="button3" @click="add(friend.id)">Add</button>
          </div>
          <div v-if="friendsFiltered.length === 0" class="text-center">
            All your friends are already in the group
          </div>
        </div>
      </div>
      <div class="space-x-2">
        <button class="button3" @click="leave">Leave</button>
        <button v-if="isOwner" class="button3" @click="deleteGroup">
          Delete
        </button>
      </div>
    </div>
  </modal>
</template>

<script>
import axios from "axios";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { computed, ref } from "vue";
import Modal from "./Modal.vue";
export default {
  components: {
    modal: Modal,
  },
  props: {
    group: Object,
    members: Array,
  },
  setup(props, { emit }) {
    const selectedIds = ref([]);
    const membersFilter = ref("");
    const friendsFilter = ref("");
    const store = useStore();
    const router = useRouter();
    const user = store.state.user;
    const friends = computed(() => store.state.friends);

    const isOwner = computed(() => user.id === props.group.owner);
    const membersFiltered = computed(() =>
      props.members.filter((m) =>
        m.username.toLowerCase().includes(membersFilter.value)
      )
    );
    const friendsFiltered = computed(() =>
      friends.value.filter(
        (f) =>
          f.username.toLowerCase().includes(friendsFilter.value) &&
          !membersFiltered.value.find((m) => m.id === f.id)
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

    const leave = async function () {
      await axios.delete("/api/v1/group/member", {
        data: { user_id: user.id, group_id: props.group.id },
      });
      store.dispatch("removeGroup", props.group.id);
      router.push("/home");
    };

    const remove = function (id) {
      emit("remove", id);
    };

    const add = function (id) {
      emit("add", id);
    };

    const deleteGroup = async function () {
      await axios.delete("/api/v1/group", {
        data: { group_id: props.group.id },
      });
      store.dispatch("removeGroup", props.group.id);
      router.push("/home");
    };

    return {
      leave,
      isOwner,
      deleteGroup,
      toggleSelected,
      remove,
      membersFilter,
      membersFiltered,
      friendsFilter,
      friendsFiltered,
      add,
    };
  },
};
</script>

<style>
</style>