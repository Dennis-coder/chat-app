<template>
  <div class="flex flex-col h-full">
    <NavbarLite :text="'Admin lounge'" :settings="false" @back="back" />
    <div class="center-me flex-col pt-4">
      <div class="w-11/12">
				<h4 class="text-lg text-center">Reports</h4>
        <div v-if="report" class="bg-gray-70 p-2 rounded-lg max-h-48 overflow-auto">
          <h4 class="text-lg underline">Plaintiff</h4>
          <p>{{ report.plaintiff.username }}</p>
          <h4 class="text-lg underline">Defendant</h4>
          <p>{{ report.defendant.username }}</p>
          <h4 class="text-lg underline">Reason</h4>
          <p>{{ report.reason }}</p>
          <h4 class="text-lg underline">Status</h4>
          <p>{{ report.status }}</p>
          <h4 class="text-lg underline">Created at</h4>
          <p>{{ report.created_at }}</p>
					<button class="button3" @click="deleteReport">Delete</button>
        </div>
				<div v-else class="bg-gray-70 p-2 rounded-lg">
					<p class="text-center">No reports left</p>
				</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import NavbarLite from "../components/NavbarLite.vue";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

export default {
  components: {
    NavbarLite,
  },
  setup() {
    const router = useRouter();
    const reports = ref([]);

    const report = computed(() =>
      reports.value.length > 0 ? reports.value[0] : null
    );

    const back = async function () {
      router.push("/home");
    };

    const loadData = async function () {
      reports.value = (await axios.get("/api/v1/report/all")).data;
    };

		const deleteReport = async function () {
			await axios.delete("/api/v1/report", { data: {
				report_id: report.value.id
			} })
			reports.value.shift()
		}

    loadData();

    return {
      report,
      back,
			deleteReport,
    };
  },
};
</script>

<style>
</style>