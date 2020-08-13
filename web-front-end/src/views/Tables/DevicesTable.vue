<template>
  <div class="card shadow" :class="type === 'dark' ? 'bg-default' : ''">
    <div
      class="card-header border-0"
      :class="type === 'dark' ? 'bg-transparent' : ''"
    >
      <div class="row align-items-center">
        <div class="col">
          <h3 class="mb-0" :class="type === 'dark' ? 'text-white' : ''">
            {{ title }}
          </h3>
        </div>
        <div class="col text-right">
          <base-button
            type="primary"
            size="sm"
            v-if="!newDeviceMode"
            @click="openModal"
            >Add Device</base-button
          >
        </div>
      </div>
    </div>
    <div>
      <modal
        :show.sync="newDeviceMode"
        body-classes="p-0"
        modal-classes="modal-dialog-centered modal-sm"
      >
        <card
          type="secondary"
          shadow
          header-classes="bg-white pb-5"
          body-classes="px-lg-5 py-lg-5"
          class="border-0"
        >
          <template>
            <div class="text-center text-muted mb-4">
              <h3>Enter device details</h3>
            </div>
            <form role="form">
              <base-input
                alternative
                class="mb-3"
                v-model="newDeviceAlias"
                placeholder="Device Alias"
                addon-left-icon="ni ni-app"
                @blur="$v.newDeviceAlias.$touch()"
                :error="isValidDeviceAliasError"
              >
              </base-input>
              <base-input
                alternative
                type="text"
                v-model="newDeviceId"
                placeholder="Device Id"
                @blur="$v.newDeviceId.$touch()"
                addon-left-icon="fa fa-barcode"
                :error="isValidDeviceIdError"
              >
              </base-input>
              <div class="text-center">
                <base-button type="danger" class="my-4" @click="closeModal"
                  >Cancel</base-button
                >
                <base-button
                  type="primary"
                  class="my-4"
                  :disabled="!isModalFormValid"
                  @click="submitNewDevice"
                  >Submit</base-button
                >
              </div>
            </form>
          </template>
        </card>
      </modal>
    </div>
    <div class="table-responsive">
      <base-table
        class="table align-items-center table-flush"
        :class="type === 'dark' ? 'table-dark' : ''"
        :thead-classes="type === 'dark' ? 'thead-dark' : 'thead-light'"
        tbody-classes="list"
        :data="deviceList"
      >
        <template slot="columns">
          <th>Device Alias</th>
          <th>Registered On</th>
          <th>Status</th>
          <th>Pulse Date</th>
          <th>Device Id</th>
          <th></th>
        </template>

        <template slot-scope="{ row }">
          <th scope="row">
            {{ row.device_registration.device_alias }}
          </th>
          <td class="budget" v-if="row.device_registration">
            {{
              new Date(row.device_registration.registration_date.$date)
                | moment('dddd, MMMM Do YYYY')
            }}
          </td>
          <td v-else>
            N/A
          </td>
          <td>
            {{ row.status | capitalize }}
          </td>
          <td v-if="row.pulse_date">
            {{ row.pulse_date.$date | moment('dddd, MMMM Do YYYY') }}
          </td>
          <td v-else>
            N/A
          </td>
          <td>
            {{ row._id.$oid }}
          </td>
          <td class="text-right">
            <base-button
              type="secondary"
              outline
              size="sm"
              icon="fa fa-times"
              @click="deregisterMode(row._id.$oid)"
              >Deregister</base-button
            >
          </td>
        </template>
      </base-table>
      <modal
        :show.sync="deleteDeviceMode"
        gradient="primary"
        modal-classes="modal-primary modal-dialog-centered"
      >
        <div class="py-3 text-center">
          <i class="ni ni-bell-55 ni-3x"></i>
          <h4 class="heading mt-4">DEREGISTER DEVICE</h4>
          <p>
            This will remove this device from your account, you will no longer
            monitor potential falls using this device.
          </p>
        </div>

        <template slot="footer">
          <base-button type="white" @click="deregisterDevice"
            >Deregister anyways</base-button
          >
          <base-button
            type="link"
            text-color="white"
            class="ml-auto"
            @click="closeDeregisterModal"
          >
            Cancel
          </base-button>
        </template>
      </modal>
    </div>
  </div>
</template>
<script>
import axios from '../../axios-auth';
import { required, alphaNum, minLength } from 'vuelidate/lib/validators';

export default {
  name: 'devices-table',
  props: {
    type: {
      type: String,
    },
    title: String,
  },
  mounted() {
    this.getUserDevices();
  },
  data() {
    return {
      deviceList: [],
      newDeviceId: null,
      newDeviceAlias: null,
      newDeviceMode: false,
      deleteDeviceMode: false,
      deleteDeviceId: null,
    };
  },
  validations: {
    newDeviceAlias: {
      required,
      minLength: minLength(5),
    },
    newDeviceId: {
      required,
      alphaNum,
      minLength: minLength(5),
    },
  },
  computed: {
    isModalFormValid() {
      return !this.$v.newDeviceAlias.$invalid && !this.$v.newDeviceId.$invalid;
    },
    isValidDeviceIdError() {
      if (this.newDeviceMode && this.$v.newDeviceId.$error) {
        return 'Must not be empty and contain at least 5 alphanumeric characters.';
      }
      return '';
    },
    isValidDeviceAliasError() {
      if (this.newDeviceMode && this.$v.newDeviceAlias.$error) {
        return 'Must not be empty and contain at least 5 characters.';
      }
      return '';
    },
  },
  methods: {
    getUserDevices() {
      axios
        .get('device/user/devices', {})
        .then(res => {
          this.setDevices(res.data);
        })
        .catch(error => this.$message.error(error.response.data.message));
    },
    setDevices(data) {
      this.deviceList = data;
    },
    closeModal() {
      this.newDeviceMode = false;
      this.newDeviceAlias = null;
      this.newDeviceId = null;
    },
    openModal() {
      this.newDeviceMode = true;
      this.$v.$reset();
    },
    submitNewDevice() {
      //post to backend
      let data = {
        deviceId: this.newDeviceId,
        deviceAlias: this.newDeviceAlias,
      };
      this.closeModal();
      axios
        .post('device/user/add', data)
        .then(res => {
          this.$message.success(res.data.message);
          this.getUserDevices();
        })
        .catch(error => this.$message.error(error.response.data.message));
    },
    deregisterMode(deviceId) {
      this.deleteDeviceId = deviceId;
      this.deleteDeviceMode = true;
    },
    closeDeregisterModal() {
      this.deleteDeviceMode = false;
      this.deleteDeviceId = null;
    },
    deregisterDevice() {
      //post to backend
      let deviceId = this.deleteDeviceId;
      this.closeDeregisterModal();
      axios
        .post('device/user/deregister/' + deviceId, {})
        .then(res => {
          this.$message.success(res.data.message);
          this.getUserDevices();
        })
        .catch(error => this.$message.error(error.response.data.message));
    },
  },
};
</script>
