<template>
  <!-- ViewAsWidget.vue
    
  -->
  <sui-dropdown :text="`Viewing as: ${name}`" v-if="viewingAsId">
    <sui-dropdown-menu class="widget-dropdown">
      <sui-dropdown-item>
        <router-link :to="`/search/All`">Change student</router-link>
      </sui-dropdown-item>
      <sui-dropdown-divider/>
      <sui-dropdown-item>
        <router-link :to="this.$route.path">Back to main view</router-link>
      </sui-dropdown-item>
    </sui-dropdown-menu>
  </sui-dropdown>
</template>

<script>
import axios from 'axios';
import { API_URL } from '@/constants';
import { mapMutations, mapState } from 'vuex';


export default {
  name: 'ViewAsWidget',
  props: {
    viewingAsId: {
      type: String,
      default: '',
    }
  },
  data() {
    return {
      name: '',
    };
  },
  computed: {
    ...mapState('auth', ['profile']),
  },
  created() {
    if (this.viewingAsId) {
      this.retrieveStudentInfo(this.viewingAsId);
    }
  },
  methods: {
    retrieveStudentInfo(studentPk) {
      axios.get(`${API_URL}/students/`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
        .then((response) => {
          const userInfo = response.data.result;

          if (userInfo.first_name) { 
            this.name = userInfo.first_name;
          }
          if (userInfo.last_name) {
            if (userInfo.first_name) { this.name += ' '; }
            this.name += userInfo.last_name; 
          }
        })
        .catch((error) => {
          
        })
        .finally(() => {

        });
    }
  },
  watch: {
    viewingAsId(newId) { // runs when data prop is updated
      if (newId) {
        this.retrieveStudentInfo(newId);
      }
    }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .widget-dropdown {
    margin-top: 10pt;
  }
  .widget-dropdown .item a {
    color: var(--color-blue-50);
  }
</style>
