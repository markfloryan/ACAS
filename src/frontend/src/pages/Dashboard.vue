<template>
  <!-- Dashboard.vue
    This is the "home" page that gives professors the option to create a class
    or select a class form the sidebar.

    This is the page a user is jumped to after a successful login/signup.
   -->
  <div class="dashboard">
    <h2 v-if="this.profile.is_professor == 0" class="title">Welcome back{{ userFullName }}</h2>
    <h2 v-if="this.profile.is_professor == 1" class="title">Welcome back, Professor {{ this.profile.last_name }}</h2>
    <Sidebar class="sidebar"/>
    <div class="content">
      <div class="call-to-action">
        <h2 class="select">Select a class</h2>
        <p  v-if="isProfessor" >or...</p>
      </div>
      <div class="actions"  v-if="isProfessor" >
        <router-link :to="'/create'" class="to-create-class-link">
          <button class="create-class btn btn-create">
            Create a new class
          </button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar';
import { mapMutations, mapState } from 'vuex';

export default {
  name: 'Dashboard',

  components: {
    Sidebar,
  },

  data() {
    return {
      isProfessor: false,
      userFullName: 'Billy Bob Joe',
    };
  },
  computed: {
    ...mapState('auth', ['profile']),
  },
  mounted() {
    this.isProfessor = this.profile.is_professor;
  },
  created() {
    
    this.userFullName = ''; 
    if (this.profile.first_name || this.profile.last_name) {
      this.userFullName += ', ';

      if (this.profile.first_name) {
        this.userFullName += this.profile.first_name;
      }
      if (this.profile.last_name) {
        if (this.profile.first_name) { this.userFullName += ' '; }
        this.userFullName += this.profile.last_name; 
      }
    } else {
      this.userFullName = '!'; // If no names, just say 'Welcome back!' 
    }
  },
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.dashboard {
  display: grid;
  grid-template-areas:
    'title title'
    'sidebar content';
  grid-template-columns: 3fr 10fr;
  grid-template-rows: min-content 1fr;
  height: 100%;
}
.title {
  grid-area: title;
}
.sidebar {
  grid-area: sidebar;
  margin-right: 18pt;
}
.content {
  grid-area: content;

  background-color: #fff;
  -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  border: 0.75pt solid rgba(34, 36, 38, 0.15);
  padding: 8pt;
  border-radius: 6pt;

  display: grid;

  grid-template-areas:
    '. . .'
    '. call-to-action .'
    '. actions .'
    '. . .';
  grid-template-rows: 1fr min-content min-content 1fr;

  height: calc(100% - 30pt);
}
.content > .call-to-action { 
  grid-area: call-to-action;
  text-align: center;
}
.content > .actions {
  grid-area: actions;
  padding-top: 8pt;
  text-align: center;
}
</style>
