<template>
  <div>
    <base-header type="gradient-primary" class="pb-6 pb-8 pt-5 pt-md-8">
    </base-header>

    <div class="container-fluid mt--7">
      <div class="row">
        <div class="col">
          <emergency-contacts-table
            title="Emergency Contacts"
          ></emergency-contacts-table>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import EmergencyContactsTable from './Tables/EmergencyContactsTable.vue';
export default {
  name: 'emergency-contacts',
  components: {
    EmergencyContactsTable,
  },
};
</script>
<style></style>
