<template>
  <div class="main" v-if="this.loaded">
    <div>
      <div v-if="students.length === 0">
        <p>No grades to show</p>
      </div>
      <div v-for="(student,n) in students" :key="`${student.name}-${n}-tab`">
        <!-- Student name  and competency -->
        <div>
          <h2 class="alignleft">{{ student.name }}</h2>
          <h3 class="alignright">{{ student.competency }}</h3>
        </div>
        <!-- Otherwise display the table -->
        <div>
          <sui-table celled>
            <sui-table-header>
              <sui-table-row>
                <sui-table-header-cell :width="10">Assignment</sui-table-header-cell>
                <sui-table-header-cell :width="2" text-align="right">Grade</sui-table-header-cell>
              </sui-table-row>
            </sui-table-header>
            <sui-table-body>
              <sui-table-row
                v-for="(assignment,i) in student.assignments"
                :key="`${assignment.name}-${i}-tab`"
              >
                <sui-table-cell>{{assignment.name}}</sui-table-cell>
                <sui-table-cell text-align="right">{{ assignment.grade }}</sui-table-cell>
              </sui-table-row>
            </sui-table-body>
          </sui-table>
        </div>
        <br>
      </div>
    </div>
    <div id="page-navigation">
        <button v-on:click="decrementPage" class="btn" style="padding: 2pt; font-size: 11pt;">Previous</button>
        <input v-model="pageField" placeholder="1" size=1>
        Page: {{ page }}
        <button v-on:click="incrementPage" class="btn" style="padding: 2pt; font-size: 11pt;" >Next</button>
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
      page: 1,
      pageField: 1,
    };
  },
  watch: {
    // When the page field. If it is a number greater than zero, change the page number
    pageField: function (val) {
      var page = parseInt(val);
      if(page != NaN && page >0){
        this.page = page;
      }
    },
    // When the page number changes, retrieve grades with that page number
    page: function (val) {
      this.retrieveGrades(val);
    } 
  },
  mounted() {},
  created() {
    this.retrieveGrades(this.page); // Retrieve the first page when the page loads
  },

  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    closeModal(event) {
      this.$emit('onClose');
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
    decrementPage(){
      if(this.page>1){
        this.page = this.page -1;
      }
    },
    incrementPage(){
      this.page = this.page +1;
    }
  },
};
</script>

<!-- CSS styling of the modal so everthing fits inside the modal where it is supposed to be -->
<style scoped>
.main {
  height: 100%;
}
.topic-modal {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1000000;
  width: 100%;
  height: 100%;
  background-color: rgba(100, 100, 100, 0.8);
}
.topic-modal > .content {
  grid-area: content;

  background-color: #fff;
  -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  border: 0.75pt solid rgba(34, 36, 38, 0.15);
  padding: 8pt;
  border-radius: 6pt;

  margin: auto;
  width: 70%;
  min-width: 525pt;
  height: 95%;

  position: relative;
  top: 50%;
  transform: perspective(0.75pt) translateY(-50%);
  padding: 18pt;

  display: grid;
  grid-template-areas:
    'title exit'
    'tabnav tabnav'
    'main main';
  grid-template-rows: min-content min-content 1fr;
  grid-template-columns: 1fr min-content;
}

.topic-modal > .content > .title {
  grid-area: title;
}
.topic-modal > .content > .tab-nav {
  grid-area: tabnav;
}
.topic-modal > .content > .main {
  grid-area: main;
}

.close-modal-button {
  cursor: pointer;
  grid-area: exit;
}
.close-modal-button:hover {
  color: var(--color-blue);
}

#page-navigation {
  position: relative;
  bottom: 0px;
  padding: 10px;
}

#page-number {
  position: absolute;
  right: 0;
  bottom: 0;
  padding: 10px;
}

h2 {
  padding: 5px;
  margin:0;
}

h3 {
  padding: 5px;
  margin:0;
}

.alignleft {
	float: left;
}

.alignright {
	float: right;
}

</style>
