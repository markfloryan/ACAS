<template>
  <!-- Sidebar.vue
    This is the sidebar that appears on the left of the page in Course.vue
    It shows the list of courses associated with the logged in user as
    a list of links to those courses

    delete class-> deletes a class based on class id
   -->
  <div class="sidebar">
    <div class="courses">
      <div v-for="course in courses"
        :key="course.name"
        class="course">
        <router-link
          :to="`/course/${course.link}`"
          :key="course.link"
          :style="{ color: course.link == $route.params.id ? 'var(--color-green-40)': 'var(--color-blue-50)' }">
          {{ course.name }}
        </router-link>
      </div>
    </div>
    <div class="actions"  v-if="isProfessor" >
        <router-link :to="'/create'">
          <button class="create-class btn btn-create" style="height:15%;width:100%">
            Create Class
          </button>
        </router-link>
          <!--
          <button v-if="!deleting" class="create-class btn btn-delete" style="height:15%;width:100%;margin-top:5px;" @click="deleteSwitch()"> 
            Delete Class
          </button>
          -->
           <button v-if="deleting" class="create-class btn btn-create" style="height:15%;width:100%;margin-top:5px;" @click="deleteClass()"> 
            Submit
          </button>
          <input class="btn" v-if="deleting" v-model="courseName" placeholder="Enter class-name" style="margin-top:5px;">
      </div>
  </div>
  
</template>

<script>
import axios from 'axios';
import { API_URL } from '@/constants';
import { mapGetters, mapState, mapMutations } from 'vuex';
export default {
  props: {
    role: {
      type: String,
      default: 'Student', // valid values: ['Student', 'Professor']
    },
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },

  data() {
    return {
      courses: [],
      deleting:false,
      courseName: '',
    };
  },
  // When the component is created, it sends an network request to our API,
  // asking for the particular list of courses they're enrolled / involved with
  created() {
    this.isProfessor = this.profile.is_professor;
    let courseData;
    const profile = JSON.parse(localStorage.getItem('profile'));
    axios.get(`${API_URL}/student/course/?id_token=${profile.auth.profile.id_token}`)
      .then((data) => {
        const studentToCourses = data.data.result;
        this.courses = studentToCourses.map((studentToCourse) => {
          const course = studentToCourse.course;
          return {
            link: course.id,
            name: course.name,
          };
        });
      })
      .catch((error) =>{})
      .finally(() => {});
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),

    //makes the input pop up, and the button swithc to submit
    deleteSwitch(){
      this.deleting=!this.deleting;
      this.openToast();
      this.setToastInfo({
        type: 'info',
        title: 'Type class name you want to delete and press submit.',

        duration: 6000,
      });
    },
    //parses the classes based on name, and finds class id
    deleteClass(){

      this.deleting=!this.deleting;
      for(let i = 0; i < this.courses.length; i++){
        if(this.courses[i].name==this.courseName){
          this.actuallyDelete(this.courses[i].link);
          
          this.$router.push('/');
          break;
        }else if((i===(this.courses.length-1))){
          this.openToast();
          this.setToastInfo({
            title: 'Couldnt remove the Course!',
            message: 'Course does not exist.',

            duration: 6000,
          });
        }
      }
    },
    // requests a delete on a course
    actuallyDelete(id){

      axios.delete(`${API_URL}/courses/${id}/?id_token=${this.profile.id_token}`)
        .then((response) => {      
          this.openToast();
          this.setToastInfo({
            type: 'success',
            title: 'Course successfully removed!',
            message: 'Class was deleted!',
            duration: 6000,
          });
          this.$router.push('/');
        })
        .catch((error) => {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Couldn\'t remove the Course!',
            message: 'Couldn\'t delete class.',
            duration: 6000,
          });
        });
    }
  }

};
</script>

<style>
  .sidebar {
    background-color: #fff;
    -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34,36,38,.15);
    box-shadow: 0 0.75pt 1.5pt 0 rgba(34,36,38,.15);
    border: 0.75pt solid rgba(34,36,38,.15);
    
    max-width: 225pt;
    max-height: 150pt;
    max-height: calc(100% - 30pt);
    padding: 8pt;
    border-radius: 6pt;

    display: grid;
    grid-template-areas:
    'courses'
    'actions';
    grid-template-rows: 1fr min-content;
  }

  .courses {
    overflow-y: scroll;
  }

  .course:first-child {
    padding: 0pt;
    padding-bottom: 6pt;
  }

  .course {
    padding: 6pt 0pt;
    border-bottom: 0.75pt solid #ddd;
  }

  .course:last-child {
    border-bottom: 0pt solid #ddd;
  }

  .course a {
    font-size: 13.5pt;
  }
</style>
