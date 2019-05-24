<template>
  <!-- Search.vue
    This is the page where search results show up.
   -->
  <div class="search">
    <h2>You searched: {{ decodeURI(this.query) }}</h2>
    <div class="content">
      <div v-for="(result, index) in results" :key="`search-result-${index}`" style="margin-bottom: 8pt;">
        <span class="course-badge">{{ formatCourse(result.course.course_code, result.course.subject_code) }}</span>
        <router-link :to="`/course/${result.course.id}/?viewAs=${result.student.id}`">
          <h3 style="display: inline-block">{{ formatName(result.student.first_name, result.student.last_name) }}</h3>
        </router-link>
        <p style="font-size: 10.75pt;">{{ result.student.email ? result.student.email : null }}</p>
      </div>
    </div>
    <LoadingLayer v-if="loading"
      :message="'Saving quiz answers...'" />
  </div>
</template>

<script>
import axios from 'axios';
import { mapMutations, mapState } from 'vuex';
import LoadingLayer from '@/components/LoadingLayer';
import Sidebar from '@/components/Sidebar';
import { API_URL } from '@/constants';

export default {
  name: 'Search',

  components: {
    LoadingLayer,
  },
  props: {
    query: {
      type: String,
      default: '',
    }
  },
  data() {
    return {
      loading: false,
      results: [],
    };
  },
  methods: {
    formatCourse(course_code, subject_code) {
      return subject_code.toUpperCase() + ' ' + course_code;
    },
    formatName(first_name, last_name) {
      let userFullName = ''; 
      if (first_name || last_name) {
        if (first_name) {
          userFullName += first_name;
        }
        if (last_name) {
          if (first_name) { userFullName += ' '; }
          userFullName += last_name; 
        }
      }
      return userFullName;
    },
    searchQuery() {
      const profile = JSON.parse(localStorage.getItem('profile'));
      this.loading = true;
      axios.get(`${API_URL}/search/?query=${this.query}&id_token=${profile.auth.profile.id_token}`)
        .then((response) => {
          this.results = response.data.result;
        })
        .catch((error) => {
          
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
  mounted() {
  },
  created() {
    this.searchQuery();
  },
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .content {
    background-color: #fff;
    -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
    box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
    border: 0.75pt solid rgba(34, 36, 38, 0.15);
    padding: 8pt;
    border-radius: 6pt;
    height: calc(100% - 30pt);
  }
  .course-badge {

  }
</style>
