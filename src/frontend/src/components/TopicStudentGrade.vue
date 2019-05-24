<!-- In this code, the vue is switched to Grades only seen by students.
First, the html checks to see the current role is a student.
Second, it checks the length of the grades array. If it is zero then it displays a small message indicating there are no resources to show at the time
Third, if the grades array is greater than 0 then it displays all the grades for that student by name and grade. It does this by retreving the student primary key then retireving the grades for the student with that primary key as seen in the Javascript below.
This is an extremely important to the client to display grades in the topic modal -->
<template>
  <div class="main" v-if="this.loaded">
    <div v-if="role === 'professor'">
      <div v-for="(student,n) in students" :key="`${student.text}-${n}-tab`">
        <!-- Student Name -->
        <h2>{{ student.text }}</h2>
        <!-- If there are no grades for a student -->
        <div v-if="grades[n].grades.length === 0">
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
                <sui-table-header-cell :width="2">Actions</sui-table-header-cell>
              </sui-table-row>
            </sui-table-header>
            <sui-table-body>
              <sui-table-row
                v-for="(grades,i) in grades[n].grades"
                :key="`${grades.value}-${i}-tab`"
              >
                <sui-table-cell>{{ grades.name }}</sui-table-cell>
                <sui-table-cell>{{ grades.category.name }}</sui-table-cell>
                <sui-table-cell text-align="right">{{ grades.value }}</sui-table-cell>
                <sui-table-cell text-align="right">{{ grades.weight }}</sui-table-cell>
                <sui-table-cell text-align="right">{{ grades.value*grades.weight }}</sui-table-cell>
                <sui-table-cell>
                  <button @click="removeGrade(n,i)">Remove</button>
                </sui-table-cell>
              </sui-table-row>
            </sui-table-body>
          </sui-table>
        </div>
      </div>
    </div>
    <div v-if="role === 'student'">
      <p>Your grade is {{ this.data.topic.ancestor_weight * 100 }}% based on previous topics</p>
      <div v-if="student_grade.length === 0">
        <p>{{ readingtext }}</p>
      </div>
      <div v-else>
        <sui-table celled>
          <sui-table-header>
            <sui-table-row>
              <sui-table-header-cell :width="12">Name</sui-table-header-cell>
              <sui-table-header-cell :width="2">Category</sui-table-header-cell>
              <sui-table-header-cell :width="4" text-align="right">Grade</sui-table-header-cell>
              <sui-table-header-cell :width="4" text-align="right">Weight</sui-table-header-cell>
              <sui-table-header-cell :width="4" text-align="right">Weighted Grade</sui-table-header-cell>
            </sui-table-row>
          </sui-table-header>
          <sui-table-body>
            <sui-table-row
              v-for="(student_grade,n) in student_grade"
              :key="`${student_grade.value}-${n}-tab`"
            >
              <sui-table-cell>{{ student_grade.name }}</sui-table-cell>
              <sui-table-cell>{{ student_grade.category.name }}</sui-table-cell>
              <sui-table-cell text-align="right">{{ student_grade.value }}</sui-table-cell>
              <sui-table-cell text-align="right">{{ student_grade.weight }}</sui-table-cell>
              <sui-table-cell text-align="right">{{ student_grade.value*student_grade.weight }}</sui-table-cell>
            </sui-table-row>
          </sui-table-body>
        </sui-table>
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
      grades: [],
      student_grade: [],
      newResource: {
        name: '',
        link: '',
      },
      readingtext: '',
      students: [],
      loaded: false,
    };
  },
  mounted() {},
  created() {
    this.getAllStudentsInTopic();
    this.retrieveStudentPK();
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

      axios
        .delete(`${API_URL}/grades/?gradeId=${grade.pk}`)
        .then(res => {
          // Need to refresh the page
          this.students = [];
          this.grades = [];
          this.getAllStudentsInTopic();
        })
        .catch(error => {
          console.log(error);
        });
    },
    getAllStudentsInTopic() {
      // console.log(this.data);
      axios
        .get(
          `${API_URL}/students_in_topic/${this.data.course.id}/${
            this.data.topic.id
          }/`
        )
        .then(student => {
          // console.log(student);
          // Save the students
          this.students = student.data;
          this.students.sort((a, b) =>
            a.value > b.value ? 1 : b.value > a.value ? -1 : 0
          );
          // console.log(this.students);
          this.students.forEach((student, n) => {
            console.log(student.text + ' ' + student.value);
            axios
              .get(`${API_URL}/grades/${student.value}/${this.topicId}`)
              .then(response => {
                // console.log(student.value);
                let temp_grades = [];
                temp_grades = response.data.result;
                // console.log(temp_grades);
                if (temp_grades.length === 0) {
                  this.readingtext = 'We could not find any grades';
                }
                this.grades.push({
                  grades: temp_grades,
                  student: student.value,
                });
                this.grades.sort((a, b) =>
                  a.student > b.student ? 1 : b.student > a.student ? -1 : 0
                );
              })
              .catch(error => {
                this.openToast();
                this.setToastInfo({
                  type: 'error',
                  title: 'Could not retrieve grades!',
                  message: 'Error on our end. Please try again later!',
                  duration: 6000,
                });
              })
              .finally(() => {});
          });

          console.log(this.grades);
          this.loaded = true;
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    retrieveStudentPK() {
      let primarykey;
      const profile = JSON.parse(localStorage.getItem('profile'));
      axios
        .get(`${API_URL}/students/?id_token=${profile.auth.profile.id_token}`)
        .then(response => {
          console.log(response.data.result.pk);
          primarykey = response.data.result.pk;
          this.retrieveGrades(primarykey);
        });
    },
    //hit api endpoint to retrieve grades
    retrieveGrades(studentPK) {
      let viewAs = '';
      if (this.$route.query && this.$route.query.viewAs) {
        viewAs = this.$route.query.viewAs;
      }
      axios
        .get(`${API_URL}/grades/${studentPK}/${this.topicId}?view_as=${viewAs}`)
        .then(response => {
          // console.log(response.data.result);
          this.student_grade = response.data.result;
          if (this.student_grade.length === 0) {
            this.readingtext = 'We could not find any grades';
          }
        })
        .catch(error => {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Could not retrieve grades!',
            message: 'Error on our end. Please try again later!',
            duration: 6000,
          });
        })
        .finally(() => {});
    },
    getStudentNameByPK(studentPK, index) {
      axios
        .get(`${API_URL}/students/${studentPK}/`)
        .then(response => {
          console.log(response.data.result);
          const student = response.data.result;
          const name = student.first_name + ' ' + student.last_name;
          this.grades[index].student = name;
          console.log(this.grades[index]);
        })
        .catch(err => {
          console.log(err);
        })
        .finally(() => {
          return 'test';
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
