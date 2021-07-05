<template>
  <div class="flex flex-col h-full">
    <NavbarLite
      v-if="group"
      :text="group.name"
      @back="back"
      @toggleSettings="toggleSettings"
    />
    <div
      v-if="group"
      class="
        max-w-sm
        w-full
        px-2
        space-y-2
        overflow-y-scroll
        pt-2
        pb-14
        mt-auto
      "
      :style="{ 'max-height': messagesHeight + 'px' }"
      ref="messagesDiv"
    >
      <Message
        v-for="message in messages"
        :key="message.id"
        :message="message"
        :class="{
          'your-message': message.senderId === user.id,
          'others-message': message.senderId !== user.id,
        }"
      />
    </div>
    <form
      class="fixed bottom-0 w-full h-12 flex bg-gray-70 bg-opacity-80 center-me"
    >
      <input
        type="text"
        placeholder="Send a message"
        class="input-field w-full rounded-full m-2 mr-14"
        v-model="text"
      />
      <button
        :disabled="text.length === 0"
        @click.prevent="sendMessage"
        class="
          absolute
          right-0
          w-9
          h-9
          center-me
          focus:outline-none
          rounded-full
          mr-2
          focus:bg-gray-400
        "
      >
        <img src="../assets/send.png" class="h-5" />
      </button>
    </form>
    <GroupSettingsModal
      v-if="showSettings"
      @close="toggleSettings"
      @remove="removeUserFromGroup"
      @add="addUserToGroup"
      :group="group"
      :members="members"
    />
  </div>
</template>

<script>
import axios from "axios";
import Message from "../components/Message.vue";
import NavbarLite from "../components/NavbarLite.vue";
import GroupSettingsModal from "../components/GroupSettingsModal.vue";
import { ref, nextTick, computed } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";

export default {
  components: {
    Message,
    NavbarLite,
    GroupSettingsModal,
  },
  setup() {
    const route = useRoute();
    const store = useStore();
    const router = useRouter();

    const messagesDiv = ref(null);

    const text = ref("");
    const messagesHeight = ref(0);
    const showSettings = ref(false);

    const group = computed(() =>
      store.state.groupsModule.groups.find(
        (group) => group.id === parseInt(route.params.id)
      )
    );
    const members = computed(() => (group.value ? group.value.members : []));
    const messages = computed(() => (group.value ? group.value.messages : []));
    const user = ref(store.state.user);
    const socket = store.state.socket;

    const sendMessage = async function () {
      let newMessage = (
        await axios.post("/api/v1/group/message", {
          text: text.value,
          group_id: group.value.id,
        })
      ).data;
      store.dispatch("addGroupMessage", newMessage);
      socket.emit(`groupMessage`, newMessage);
      text.value = "";
      scrollDown();
    };

    const resizeEvent = function () {
      messagesHeight.value = window.innerHeight - 48;
    };

    const scrollDown = async function () {
      nextTick(async () => {
        if (messagesDiv.value) {
          messagesDiv.value.scrollTop = messagesDiv.value.scrollHeight;
        } else {
          await new Promise((r) => setTimeout(r, 50));
          scrollDown();
        }
      });
    };

    const toggleSettings = function () {
      showSettings.value = !showSettings.value;
    };

    const back = function () {
      router.push("/home");
    };

    const removeUserFromGroup = async function (id) {
      try {
        await axios.delete("/api/v1/group/member", {
          data: { user_id: id, group_id: group.value.id },
        });
        let index = members.value.findIndex((m) => m.id === id);
        members.value.splice(index, 1);
        socket.emit("removeUserFromGroup", group.value.id, id);
      } catch (error) {
        console.error(error)
      }
    };

    const addUserToGroup = async function (id) {
      try {
        let member = (
          await axios.post("/api/v1/group/member", {
            user_id: id,
            group_id: group.value.id,
          })
        ).data;
        store.dispatch('addUserToGroup', {groupId: group.value.id, user: member})
        socket.emit('addUserToGroup', group.value, member)
      } catch (error) {
        console.error(error)
      }
    };

    window.addEventListener("resize", resizeEvent);
    nextTick(() => {
      resizeEvent();
      scrollDown();
    });

    return {
      group,
      user,
      text,
      messagesHeight,
      messagesDiv,
      sendMessage,
      toggleSettings,
      showSettings,
      back,
      removeUserFromGroup,
      addUserToGroup,
      members,
      messages,
    };
  },
};
</script>

<style>
</style>