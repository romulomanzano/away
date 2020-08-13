<template>
  <div class="row justify-content-center">
    <div class="col-lg-5 col-md-7">
      <div class="card bg-secondary shadow border-0">
        <div class="card-body px-lg-5 py-lg-5">
          <div class="text-center text-muted mb-4">
            <small>Sign in with credentials</small>
          </div>
          <form role="form">
            <base-input
              v-model="email"
              @blur="$v.email.$touch()"
              alternative
              class="mb-3"
              placeholder="Email"
              addon-left-icon="ni ni-email-83"
              name="email"
              :error="invalidEmail"
            >
            </base-input>

            <base-input
              v-model="password"
              alternative
              class="mb-3"
              @blur="$v.password.$touch()"
              type="password"
              name="password"
              placeholder="Password"
              addon-left-icon="ni ni-lock-circle-open"
              :error="invalidPassword"
            >
            </base-input>

            <div class="text-center">
              <base-button
                :disabled="!isValidForm"
                type="primary"
                @click="submitForm"
                class="my-4"
                >Sign In</base-button
              >
            </div>
          </form>
        </div>
      </div>
      <div class="row mt-3">
        <div class="col-6">
          <a href="#" class="text-light"><small>Forgot password?</small></a>
        </div>
        <div class="col-6 text-right">
          <router-link to="/register" class="text-light"
            ><small>Create new account</small></router-link
          >
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { email, required, minLength } from 'vuelidate/lib/validators';
import axios from '../axios-auth';

export default {
  name: 'login',
  data: () => ({
    email: null,
    password: null,
  }),
  validations: {
    email: {
      required,
      email,
    },
    password: {
      required,
      minLength: minLength(8),
    },
  },
  computed: {
    isValidForm() {
      return !this.$v.email.$invalid && !this.$v.password.$invalid;
    },
    invalidEmail() {
      if (this.$v.email.$error) {
        return 'Please enter a valid email.';
      }
      return '';
    },
    invalidPassword() {
      if (this.$v.password.$error) {
        return 'Password must contain at least 8 characters.';
      }
      return '';
    },
  },
  methods: {
    clearForm() {
      this.email = null;
      this.password = null;
    },
    async submitForm() {
      if (this.isValidForm) {
        await axios
          .post('auth/login', {
            email: this.email,
            password: this.password,
          })
          .then(res => {
            this.$store.dispatch('login', res.data);
          })
          .catch(error => {
            this.$message.error(error.response.data.message);
            this.clearForm();
            this.$v.$reset();
          });
      }
    },
  },
};
</script>
<style></style>
