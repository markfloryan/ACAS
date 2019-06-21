<!-- In this code, the vue is switched to Grades only seen by students.
First, the html checks to see the current role is a student.
Second, it checks the length of the grades array. If it is zero then it displays a small message indicating there are no resources to show at the time
Third, if the grades array is greater than 0 then it displays all the grades for that student by name and grade. It does this by retreving the student primary key then retireving the grades for the student with that primary key as seen in the Javascript below.
This is an extremely important to the client to display grades in the topic modal -->
<template>
  <div class="main" v-if="this.loaded">
    <div>
      <div v-for="(student,n) in students" :key="`${student.text}-${n}-tab`">
        <!-- Student Name -->
        <h2>{{ student.text }}</h2>
        <!-- If there are no grades for a student -->
        <div v-if="grades[student.value].grades.length === 0">
          <p>{{ readingtext }}</p>
        </div>
        <!-- Otherwise display the table -->
        <div v-else>
          <sui-table celled>
            <sui-table-header>
              <sui-table-row>
                <sui-table-header-cell :width="10">Name</sui-table-header-cell>
                <sui-table-header-cell :width="2">Category</sui-table-header-cell>
                <sui-table-header-cell :width="2" text-align="right">Grade</sui-table-header-cell>
                <sui-table-header-cell :width="4" text-align="right">Weight</sui-table-header-cell>
                <sui-table-header-cell :width="4" text-align="right">Weighted Grade</sui-table-header-cell>
              </sui-table-row>
            </sui-table-header>
            <sui-table-body>
              <sui-table-row
                v-for="(grade,i) in grades[student.value].grades"
                :key="`${student.text}-${i}-tab`"
              >
                <sui-table-cell>{{ grade.name }}</sui-table-cell>
                <sui-table-cell>{{ grade.category.name }}</sui-table-cell>
                <sui-table-cell text-align="right">{{ grade.value }}</sui-table-cell>
                <sui-table-cell text-align="right">{{ grade.weight }}</sui-table-cell>
                <sui-table-cell text-align="right">{{ grade.value*grade.weight }}</sui-table-cell>
              </sui-table-row>
            </sui-table-body>
          </sui-table>
        </div>
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
      grades: {},
      newResource: {
        name: '',
        link: '',
      },
      readingtext: 'Retrieving grades...',
      students: [],
      loaded: false,
    };
  },
  mounted() {},
  created() {
    this.retrieveGrades();
  },

  //retrieveStudentPK collects the profile by using the profiles id token
  //the primary key is sent to the console to ensure the right token was collected
  //This is important because we are going to need the student primary key for the next method

  //retrieveGrades takes in the primary key and uses an axios get request to
  //retrieve the information surrounding the grades like the value of the grade, student primary key for that grade, the primary key for the grade, name of the grade, etc.
  //This is important because we need this array of data to store in the grades array above to properly display the information
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    closeModal(event) {
      this.$emit('onClose');
    },
    // Removes a grade for a student
    removeGrade(i, n) {
      // Grab the student and the grade
      const student = this.students[i];
      const grade = this.grades[i].grades[n];

      const profile = JSON.parse(localStorage.getItem('profile'));

      axios
        .delete(`${API_URL}/grades/?gradeId=${grade.pk}/?id_token=${profile.auth.profile.id_token}`)
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
    retrieveGrades() {
      
      const profile = JSON.parse(localStorage.getItem('profile'));

      //Grab the students first
      axios
        .get(
          `${API_URL}/coursetopictostudent/${this.data.course.id}/${this.data.topic.id}/?id_token=${profile.auth.profile.id_token}`
        )
        .then(studentResponse => {

          //Save students in the array and sort it
          this.students = studentResponse.data;
          this.students.sort((a, b) =>
            a.value > b.value ? 1 : b.value > a.value ? -1 : 0
          );

          this.students.forEach((student, n) => {
            
            //initialize each student with an empty list of grades
            this.grades[student.value] = 
              {
                grades: [],
                student: student.value,
              };
          });

          axios
            .get(`${API_URL}/grades/${this.data.course.id}/${this.topicId}/?id_token=${profile.auth.profile.id_token}`)
            .then(gradesResponse => {

              var allGrades = gradesResponse.data.result;
              allGrades.forEach((grade,n) => {

                this.grades[grade.student].grades.push(grade);
              });

            })
            .catch(error => {
              console.log(error);
              this.openToast();
              this.setToastInfo({
                type: 'error',
                title: 'Could not retrieve grades!',
                message: 'Error on our end. Please try again later!',
                duration: 6000,
              });
            })
            .finally(() => {
              this.loaded=true;

            });
      })
      .catch(error => {
        console.log(error);
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Could not retrieve grades!',
          message: 'Error on our end. Please try again later!',
          duration: 6000,
        });
      })
      .finally(() => {
        
      });
    },
  },
};
</script>

<!-- CSS styling of the modal so everthing fits inside the modal where it is supposed to be -->
<style scoped>
.main {
  overflow-y: scroll;
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
</style>
