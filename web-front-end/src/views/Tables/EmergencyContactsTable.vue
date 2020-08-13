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
            v-if="!modalContactMode"
            @click="openModal"
            >Add Emergency Contact</base-button
          >
        </div>
      </div>
    </div>
    <div>
      <modal
        :show.sync="modalContactMode"
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
              <h3>Enter Contact details</h3>
            </div>
            <form role="form">
              <base-input
                alternative
                class="mb-3"
                v-model="modalContactFirstName"
                placeholder="First Name"
                @blur="$v.modalContactFirstName.$touch()"
                :error="isValidFirstNameError"
              >
              </base-input>

              <base-input
                alternative
                class="mb-3"
                v-model="modalContactLastName"
                placeholder="Last Name"
                @blur="$v.modalContactLastName.$touch()"
                :error="isValidLastNameError"
              >
              </base-input>

              <base-input
                alternative
                class="mb-3"
                v-model="modalContactRelationship"
                placeholder="Relationship"
                @blur="$v.modalContactRelationship.$touch()"
                :error="isValidRelationshipError"
              >
              </base-input>
              <base-input
                alternative
                placeholder="8888888888"
                input-classes="form-control-alternative"
                @blur="$v.modalContactPhoneNumber.$touch()"
                v-model="modalContactPhoneNumber"
                type="tel"
                :error="isValidPhoneNumberError"
                maxlength="10"
              />
              <div class="text-center">
                <base-button type="danger" class="my-4" @click="closeModal"
                  >Cancel</base-button
                >
                <base-button
                  type="primary"
                  class="my-4"
                  :disabled="!isModalFormValid"
                  @click="submitContact"
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
        :data="contactList"
      >
        <template slot="columns">
          <th>First Name</th>
          <th>Last Name</th>
          <th>Relationship</th>
          <th>Phone Number</th>
          <th></th>
        </template>

        <template slot-scope="{ row }">
          <th scope="row">
            {{ row.first_name | capitalize }}
          </th>
          <th scope="row">
            {{ row.last_name | capitalize }}
          </th>
          <th scope="row">
            {{ row.relationship | capitalize }}
          </th>
          <th scope="row">
            {{ row.phone_number }}
          </th>

          <td class="text-right">
            <base-button
              type="primary"
              outline
              size="sm"
              icon="fa fa-pen"
              @click="editMode(row)"
              >Edit</base-button
            >
            <base-button
              type="danger"
              outline
              size="sm"
              icon="fa fa-trash"
              @click="archiveMode(row._id.$oid)"
              >Archive</base-button
            >
          </td>
        </template>
      </base-table>
      <modal
        :show.sync="archiveContactMode"
        gradient="primary"
        modal-classes="modal-primary modal-dialog-centered"
      >
        <div class="py-3 text-center">
          <i class="ni ni-bell-55 ni-3x"></i>
          <h4 class="heading mt-4">Archive Contact</h4>
          <p>
            This will archive this contact, we will no longer be able to alert
            this person should an emergency occur.
          </p>
        </div>

        <template slot="footer">
          <base-button type="white" @click="archiveContact"
            >Archive anyways</base-button
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
import { required } from 'vuelidate/lib/validators';

const isValidStringWithSpaces = value => /^[a-zA-Z\s]*$/.test(value);
const isPhone = value => /^[0-9]{10}$/.test(value);

export default {
  name: 'emergency-contacts-table',
  props: {
    type: {
      type: String,
    },
    title: String,
  },
  mounted() {
    this.getUserEmergencyContacts();
  },
  data() {
    return {
      contactList: [],
      modalContactFirstName: null,
      modalContactLastName: null,
      modalContactPhoneNumber: null,
      modalContactRelationship: null,
      modalContactMode: false,
      archiveContactMode: false,
      archiveContactId: null,
      editContactId: null,
    };
  },
  validations: {
    modalContactFirstName: {
      required,
      isName: isValidStringWithSpaces,
    },
    modalContactLastName: {
      required,
      isName: isValidStringWithSpaces,
    },
    modalContactRelationship: {
      required,
      isName: isValidStringWithSpaces,
    },
    modalContactPhoneNumber: {
      required,
      phoneValid: isPhone,
    },
  },
  computed: {
    isModalFormValid() {
      return (
        !this.$v.modalContactFirstName.$invalid &&
        !this.$v.modalContactLastName.$invalid &&
        !this.$v.modalContactPhoneNumber.$invalid &&
        !this.$v.modalContactRelationship.$invalid
      );
    },
    isValidFirstNameError() {
      if (this.modalContactMode && this.$v.modalContactFirstName.$error) {
        return 'Must not be empty and only contain letters.';
      }
      return '';
    },
    isValidLastNameError() {
      if (this.modalContactMode && this.$v.modalContactLastName.$error) {
        return 'Must not be empty and only contain letters.';
      }
      return '';
    },
    isValidRelationshipError() {
      if (this.modalContactMode && this.$v.modalContactRelationship.$error) {
        return 'Must not be empty and only contain letters.';
      }
      return '';
    },
    isValidPhoneNumberError() {
      if (this.modalContactMode && this.$v.modalContactPhoneNumber.$error) {
        return 'Invalid Number.';
      }
      return '';
    },
  },
  methods: {
    getUserEmergencyContacts() {
      axios
        .get('emergency/user/contacts', {})
        .then(res => {
          this.setContacts(res.data);
        })
        .catch(error => this.$message.error(error.response.data.message));
    },
    setContacts(data) {
      this.contactList = data;
    },
    closeModal() {
      this.modalContactMode = false;
      this.modalContactFirstName = null;
      this.modalContactLastName = null;
      this.modalContactRelationship = null;
      this.modalContactPhoneNumber = null;
    },
    openModal() {
      this.modalContactMode = true;
      this.$v.$reset();
    },
    submitContact() {
      //post to backend
      let data = {
        modalContactFirstName: this.modalContactFirstName,
        modalContactLastName: this.modalContactLastName,
        modalContactRelationship: this.modalContactRelationship,
        modalContactPhoneNumber: this.modalContactPhoneNumber,
      };
      this.closeModal();
      //depending of the value either post new or update contact
      if (!this.editContactId) {
        axios
          .post('emergency/user/contact/add', data)
          .then(res => {
            this.$message.success(res.data.message);
            this.getUserEmergencyContacts();
          })
          .catch(error => this.$message.error(error.response.data.message));
      } else {
        axios
          .put('emergency/user/contact/' + this.editContactId + '/edit', data)
          .then(res => {
            this.$message.success(res.data.message);
            this.getUserEmergencyContacts();
            this.editContactId = null;
          })
          .catch(error => this.$message.error(error.response.data.message));
      }
    },
    archiveMode(contactId) {
      this.archiveContactId = contactId;
      this.archiveContactMode = true;
    },
    editMode(row) {
      this.modalContactMode = true;
      this.editContactId = row._id.$oid;
      this.$v.$reset();
      //set to pre-existing values
      this.modalContactFirstName = row.first_name;
      this.modalContactLastName = row.last_name;
      this.modalContactRelationship = row.relationship;
      this.modalContactPhoneNumber = row.phone_number;
    },
    closeDeregisterModal() {
      this.archiveContactMode = false;
      this.archiveContactId = null;
    },
    archiveContact() {
      //post to backend
      let contactId = this.archiveContactId;
      this.closeDeregisterModal();
      axios
        .post('emergency/user/contact/' + contactId + '/archive', {})
        .then(res => {
          this.$message.success(res.data.message);
          this.getUserEmergencyContacts();
        })
        .catch(error => this.$message.error(error.response.data.message));
    },
  },
};
</script>
