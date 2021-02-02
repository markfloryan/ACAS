<template>
  <!--
    This is the main page for viewing the details of a class
    THis is where ClassGraph.vue is rendered as well as the option to add students to the course
    or edit the graph for the class
  -->
  <div class="dashboard">
    <!-- Course Selected -->
    <h2 class="title">Class - {{ classData.name ? classData.name : this.id}}</h2>
    
    <!-- Top action buttons-->
    <div class="actions">
      <button
        v-if="isProfessor"
        class="btn btn-plain edit-btn"
        style="margin-left: 8pt;"
        @click="pullGrades()"
      >Update grades</button>
      <button
        v-if="isProfessor"
        class="btn btn-plain edit-btn"
        style="margin-left: 8pt;"
        @click="toEdit()"
      >Edit graph</button>
      <button
        v-if="isProfessor && context !== 'courseRoster'"
        class="btn btn-primary edit-btn"
        :style="returnPrimaryButtonStyle"
        @click="changeContext('courseRoster')"
      >Roster</button>
      <button
        v-if="isProfessor && context !== 'csvUpload'"
        class="btn btn-primary edit-btn"
        :style="returnPrimaryButtonStyle"
        @click="changeContext('csvUpload')"
      >CSV</button>
      <button
        v-if="isProfessor && context !== 'classGraph'"
        class="btn btn-primary edit-btn"
        :style="returnPrimaryButtonStyle"
        @click="changeContext('classGraph')"
      >Back to graph</button>
      <h3
        id="grade"
        v-if="!isProfessor"
        data-toggle="tooltip"
        data-placement="bottom"
        :title="'Nodes at mastery: ' + this.numNodesMast + ' | competency: ' + this.numNodesComp"
        @click="clickGradeModal('TODO:')"
      >Grade: {{this.letterGrade}}
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-question-circle" viewBox="0 0 16 16">
        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"></path>
        <path d="M5.255 5.786a.237.237 0 0 0 .241.247h.825c.138 0 .248-.113.266-.25.09-.656.54-1.134 1.342-1.134.686 0 1.314.343 1.314 1.168 0 .635-.374.927-.965 1.371-.673.489-1.206 1.06-1.168 1.987l.003.217a.25.25 0 0 0 .25.246h.811a.25.25 0 0 0 .25-.25v-.105c0-.718.273-.927 1.01-1.486.609-.463 1.244-.977 1.244-2.056 0-1.511-1.276-2.241-2.673-2.241-1.267 0-2.655.59-2.75 2.286zm1.557 5.763c0 .533.425.927 1.01.927.609 0 1.028-.394 1.028-.927 0-.552-.42-.94-1.029-.94-.584 0-1.009.388-1.009.94z"></path>
      </svg>
      </h3>
        
    </div>

    <!-- Variable Content -->
    <Sidebar class="sidebar"/>
    <div class="content">
      <CourseRoster
        v-if="context === 'courseRoster'"
        :courseId="id"
        @contextChange="changeContext"
      />
      <CSVUpload
        v-if="context === 'csvUpload'"
        :courseId="id"
        @contextChange="changeContext"
      />
      <!-- TODO: What does id="3" mean? Is it hardcoded? -->
      <ClassGraph
        :hidden="context !== 'classGraph'"
        :id="3" 
        :role="isProfessor ? 'professor' : 'student'"
        :data="graphData"
        @onClose="retrieveClassGraph"
      />
      <h1
        v-if="classNotFound && !isLoading"
        style="text-align: center; margin: auto;"
      >No class graph found :(</h1>
      <LoadingLayer v-if="isLoading" :message="'Fetching course...'"/>
    </div>
    <CourseGradeModal
      :isOpen="courseGradeModalIsOpen"
      :role="isProfessor ? 'professor' : 'student'"
      :data="classData"
      :id="id"
      :letterGrade="letterGrade"
      :numNodesMast="numNodesMast"
      :numNodesComp="numNodesComp"
      @onClose="courseGradeModalIsOpen = false; $emit('onClose');" />
  </div>
</template>



<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import CSVUpload from '@/components/CSVUpload';
import CourseRoster from '@/components/CourseRoster';
import ClassGraph from '@/components/ClassGraph';
import LoadingLayer from '@/components/LoadingLayer';
import Sidebar from '@/components/Sidebar';
import { API_URL } from '@/constants';
import { lockTree } from '@/components/NodeLock';
import CourseGradeModal from '@/components/CourseGradeModal';

export default {
  name: 'Course',
  components: {
    CSVUpload,
    CourseRoster,
    ClassGraph,
    LoadingLayer,
    Sidebar,
    CourseGradeModal,
  },
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  data() {
    return {
      classNotFound: true,
      context: 'classGraph',
      classData: {},
      graphData: {},
      isLoading: false,
      isProfessor: false,
      numberofNodes: 0,
      totalgrade: 0, // TODO: Deprecated use of grade % not letter grade
      letterGrade: '?',
      numNodesMast: 0,
      numNodesComp: 0,
      numNodesLocked: 0,
      file: '',
      courseGradeModalIsOpen: false,
    };
  },
  created() {
    this.retrieveClassGraph();
  },
  methods: {
    changeContext(newContext) {
      this.context = newContext;
    },
    retrieveClassGraph() {
      // Maybe check if data in vuex, load from there,
      // if not make GET request and then store in vuex?
      this.isProfessor = this.profile.is_professor;
      this.isLoading = true;
      let viewAs = '';
      if (this.$route.query && this.$route.query.viewAs) {
        viewAs = this.$route.query.viewAs;
      }
      axios
        .get(
          `${API_URL}/student/course/?courseId=${
            this.id
          }&view_as=${viewAs}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } }
        )
        .then(data => {
          this.classNotFound = false;
          let classData = data.data.result;
          this.totalgrade = classData.grade;
          
          lockTree(classData);
          
          this.numNodesLocked = 0;
          this.numNodesComp = 0;
          this.numNodesMast = 0;
          
          classData.nodes.forEach((node) => {
            //console.log(JSON.stringify(node, null,4));
            if (node.topic.locked) // TODO: Node isn't actually locked
              this.numNodesLocked++;
            else if (node.competency == 1)
              this.numNodesComp++;
            else if (node.competency == 2)
              this.numNodesMast++;
          });
          this.letterGrade = classData.letterGrade;
          classData = {
            pk: classData.course.pk,
            name: classData.course.name,
            course_code: classData.course.course_code,
            subject_code: classData.course.subject_code,
            nodes: classData.nodes,
            edges: classData.edges,
          };
          // Loop through all nodes and sum progress
          classData.nodes = classData.nodes.map(node => {
            return {
              ...node,
              id: node.pk,
              grade: node.grade,
            };
          });
          this.graphData = classData;
          this.classData = {
            uuid: classData.pk,
            name: classData.name,
            courseCode: classData.course_code,
            subjectCode: classData.subject_code,
          };
        })
        .catch(error => {
          console.log(error);
          this.classNotFound = true;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    toEdit() {
      this.$router.push({ name: 'Edit', params: { id: this.id } });
    },
    pullGrades() {
      let localID = this.profile.id_token;
      let coursePK = this.id;
      axios
        .get( `${API_URL}/courseGradescopeUpload/${coursePK}`,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              Authorization: `Bearer ${this.profile.id_token}`
            }
          }
        ).then((response)=> {
          if(response.data.ok) {
            this.openToast();
            this.setToastInfo({
              type: 'success',
              title: 'Successful Pull',
              message: 'Grades added to gradebook',
              duration: 5000,
            });
          }
          else {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Pulling Error',
              message: `${response.data.errors}`,
              duration: 10000,
            });
          }
        /*
        setTimeout(function(){ 
          openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Uploading Error',
            message: `${response.data.errors[1]}`,
            duration: 6000,
        }); }, 6000);*/
          //}
      
        })
        .catch(function(){
          console.log(`${API_URL}/courseGradesUpload/${coursePK}`);
          console.log('FAILURE');
        });
    },
    clickGradeModal(data) {
      this.courseGradeModalIsOpen = true;
    },
    
    ...mapMutations(
      'toast',
      ['openToast', 'setToastInfo'],
    ),
  },
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.dashboard {
  display: grid;
  grid-template-areas:
    'title title actions'
    'sidebar content content';
  grid-template-columns: 3fr 3fr 7fr;
  grid-template-rows: min-content 1fr;
  height: 100%;
}
.title {
  grid-area: title;
}
.actions {
  grid-area: actions;
}
.actions button {
  float: right;
  white-space: nowrap;
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
  border-radius: 6pt;
  height: calc(100% - 30pt);
  position: relative;
}
#grade {
  float: right;
  display: inline-block;
  transform: translateY(50%);
  margin: auto;
  padding-right: 8pt;
}
</style>
