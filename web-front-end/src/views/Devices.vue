<template>
  <div>
    <base-header type="gradient-primary" class="pb-6 pb-8 pt-5 pt-md-8">
    </base-header>

    <div class="container-fluid mt--7">
      <div class="row">
        <div class="col">
          <devices-table title="Registered Devices"></devices-table>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import DevicesTable from './Tables/DevicesTable';
export default {
  name: 'devices',
  components: {
    DevicesTable,
  },
};
</script>
<style></style>
