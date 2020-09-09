<template>
  <div class="login-card">
    <div class="left">
      <div class = "logo-container">
     <!-- project logo -->
      <router-link to="/" class="logo">
          <img 
            class="logos"
            height="120"
            width="120"
            src="../assets/logo2.jpg" />
        </router-link>
      
      </div>
    </div>
    <div class="right">
      <div class="message">
        <p style="font-weight: bold; font-size: 18pt; margin-bottom: 3pt;">Hello</p>
        <!-- Login -->
        <p v-if="!isSignUp"> Sign in with google below</p>
        <!-- Signup -->
        <p v-if="isSignUp"> Sign up with google below</p>
      </div>

      <!-- This version of logging in works with Chrome and Safari, but not Firefox -->

      <!-- Sign in -->
      <div v-if="!isSignUp" id="googleSignInButton" class="g-signin-button" @click="signIn">
        <p>Sign In</p>
      </div>

      <!-- Debug Professor Sign in -->
      <div v-if="!isSignUp && debugLogin" id="debugProfSignIn" class="g-signin-button" @click="debugProfSignIn">
        <p>Debug Prof Sign In</p>
      </div>

      <!-- Debug Student Sign in -->
      <div v-if="!isSignUp && debugLogin" id="debugStudSignIn" class="g-signin-button" @click="debugStudSignIn">
        <p>Debug Stud Sign In</p>
      </div>

      <!-- Sign Up -->
      <div v-if="isSignUp" id="studentButton" class="g-signin-button" @click="signUp(false)">
        <p>Create Account</p>
      </div>
      
      <!-- switch from signin to signup-->
    <div v-if="!isSignUp" class="center-signup">
      <a @click="navigateSignUp ">or sign up</a>
    </div>
    <!-- switch from signup to signin-->
    <div v-if="isSignUp" class="center-signin">
      <a @click="navigateSignIn">or sign in</a>
    </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

import { mapState, mapActions, mapGetters, mapMutations } from 'vuex';
import store from '../vuex';

export default {
  name: 'LoginCard',
  data() {
    return {
      loading: true,
      localsignup:this.isSignUp,
      debugLogin: true,
    };
  },
  computed: {
    ...mapState({
      signedIn: state => state.auth.signedIn,
      profile: state => state.auth.profile,
    }),
    ...mapGetters('auth', ['isSignedIn']),
  },
  mounted() {
    var self = this;
    store.dispatch('auth/isSignedIn').then(() => {
      self.loading = false;
    });
    
  },
  watch: {
    isSignedIn(newValue, oldValue) {
      if (newValue) {
        this.$router.push('/');
        this.openToast();
        this.setToastInfo({
          type: 'success',
          title: 'Welcome!',
        });
      }

    //axios.get(`${API_URL}/settings/${pk}`);
    },
  },
  methods: {
    ...mapActions('auth', ['signIn', 'signUp', 'debugProfSignIn', 'debugStudSignIn']),
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    navigateSignUp() {
      //sets url to signup
      this.$router.push('/signup');
    },
    //sets url to welcome (signin)
    navigateSignIn() {
      this.$router.push('/welcome');
    },

  },
  // data prop where it is passed in from another component
  props: ['isSignUp'],
};
</script>

<style>
.g-signin-button {
  /* This is where you control how the button looks. Be creative! */
  display: inline-block;
  padding: 3pt 6pt;
  border-radius: 2.25pt;
  background-color: #3c82f7;
  color: #fff;
  box-shadow: 0 2.25pt 0 #0f69ff;
}
.login-card {
  height: 150pt;
  width: 300pt;
  margin: auto;
  margin-top: 20vh !important;
  display: grid;
  grid-template-areas: 'left right';
  grid-template-columns: 2fr 3fr;
  border-radius: 0.28571429rem !important;
  -webkit-box-shadow: 0 0.75pt 2.25pt 0 #d4d4d5, 0 0 0 0.75pt #d4d4d5;
  box-shadow: 0 0.75pt 2.25pt 0 #d4d4d5, 0 0 0 0.75pt #d4d4d5;
  background-color: white;
}
.login-card .left {
  grid-area: left;
  border-radius: 0.28571429rem 0pt 0pt 0.28571429rem !important;
  background-color: dodgerblue;
}
.login-card .right {
  grid-area: right;
  display: grid;
  grid-template-areas:
    'message'
    'g-signin-button';

  padding: 8pt;
}
.message {
  grid-area: message;
  text-align: center;
}
.g-signin-button {
  grid-area: 'g-signin-button';
  padding: 6pt;
  font-size: 10.5pt;
  display: inherit;
  width: 112.5pt;
  text-align: center;
  cursor: pointer;
  margin: auto;
}
.g-signin-button > p {
  color: white;
}
.logos {
  margin-top:24%;
  margin-left:13%;
   height:120;
   width:120;
   border-radius:4px;
  

}
.center-signup{
  margin-left:35%;
}
.center-signin{
  margin-left:35%;
}

</style>
