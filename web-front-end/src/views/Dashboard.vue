<template>
  <div>
    <base-header type="gradient-primary" class="pb-6 pb-8 pt-5 pt-md-8">
      <!-- Card stats -->
      <div class="row">
        <div class="col-xl-4 col-lg-6">
          <stats-card
            title="Total Events detected"
            type="gradient-primary"
            v-bind:sub-title="eventsDetected | formatNumber"
            icon="ni ni-sound-wave"
            class="mb-4 mb-xl-0"
          >
          </stats-card>
        </div>
        <div class="col-xl-4 col-lg-6">
          <stats-card
            title="Number of Active Devices"
            type="gradient-default"
            :sub-title="activeDevices | formatNumber"
            icon="ni ni-laptop"
            class="mb-4 mb-xl-0"
          >
          </stats-card>
        </div>
        <div class="col-xl-4 col-lg-6">
          <stats-card
            title="Emergency Readiness"
            type="gradient-danger"
            :sub-title="emergencyReadiness | formatPercentage"
            icon="ni ni-ambulance"
            class="mb-4 mb-xl-0"
          >
          </stats-card>
        </div>
      </div>
    </base-header>
  </div>
</template>
<script>
import axios from '../axios-auth';

export default {
  data() {
    return {
      eventsDetected: 0,
      activeDevices: 0,
      emergencyReadiness: 0,
    };
  },
  methods: {
    getAccountSummary() {
      axios
        .get('profile/user/account_summary', {})
        .then(res => {
          this.setSummary(res.data);
        })
        .catch(error => this.$message.error(error.response.data.message));
    },
    setSummary(data) {
      this.eventsDetected = data.events_detected;
      this.activeDevices = data.active_device_count;
      this.emergencyReadiness = data.readiness_score;
    },
  },
  mounted() {
    this.getAccountSummary();
  },
};
</script>
<style></style>
