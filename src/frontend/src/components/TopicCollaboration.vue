<!-- View for students to collaborate -->
<template>
  <div class="main">
    
    <div v-if="true" style="margin-top: 8pt; overflow-y: scroll">

      <div class="center">
          <button v-on:click="helperToggle" class="btn btn-primary" style="font-size: 30px; margin-right: 16pt;">I can help</button>
          <button v-on:click="helpeeToggle" class="btn btn-primary" style="font-size: 30px; margin-left: 16pt;">I need help</button>
        <h2 class="" align="left">Standing</h2>
        <h2 class="" align="right">Standing</h2>
      </div>
    </div>
  </div>
</template>

<script>
//importing important functionalities for this vue
import axios from 'axios';
import { mapGetters, mapMutations } from 'vuex';
import { API_URL } from '@/constants';

export default {
  components: {},
  props: {
    role: {
      type: String,
      default: 'student',
    },
    data: {
      type: Object,
    },
    topicId: {
      type: Number,
    },
  },
  //this is where the array that is retrieved using axios
  //is saved. Making it easier to parse the information in
  //the HTML above. This is important to do so data does not get lost
  data() {
    return {
      newResource: {
        name: '',
        link: '',
      },
      students: [],
      loaded: false,

    };
  },
  watch: {
     
  },
  mounted() {},
  created() {
    // TODO: Grab collaboration status for node
  },

  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    closeModal(event) {
      this.$emit('onClose');
    },
    
    // adjust url whether removing a helper or helpee
    remove(type) {

    },

    add(type) {
        
    },
    
    // Removes a grade for a student. Currently outdated
    removeGrade(i, n) {
      // Grab the student and the grade
      const student = this.students[i];
      const grade = this.grades[i].grades[n];

      const profile = JSON.parse(localStorage.getItem('profile'));

      axios
        .delete(`${API_URL}/grades/?gradeId=${grade.pk}/`,  { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } })
        .then(res => {
          // Need to refresh the page
          this.students = [];
          this.grades = {};
          this.getAllStudentsInTopic();
        })
        .catch(error => {
          console.log(error);
        });
    },
    //hit api endpoint to retrieve grades
    retrieveGrades(page) {
      
      const profile = JSON.parse(localStorage.getItem('profile'));

      //Grab the students first
      axios
        .get(
          `${API_URL}/coursetopictostudent/${this.data.course.id}/${this.data.topic.id}/?page=${page}`,  { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } }
        )
        .then(studentResponse => {

          //Save students in the array and sort it
          this.students = studentResponse.data;
        })
        .catch(error => {
          console.log(error);
          //     this.openToast();
          //     this.setToastInfo({
          //       type: 'error',
          //       title: 'Could not retrieve grades!',
          //       message: 'Error on our end. Please try again later!',
          //       duration: 6000,
          //     });
        })
        .finally(() => {
          this.loaded=true;
        });
    },
  },
};
</script>