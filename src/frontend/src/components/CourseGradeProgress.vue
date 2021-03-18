<!-- View for student to plan their desired grade and keep on track -->
<template>
  <div class="main">
    
    <div v-if="true" style="margin-top: 8pt;"> 
      <sui-form v-if="role != 'professor'" @submit.prevent>
        <sui-form-field v-if="true">
          <h2>Target Grade</h2>
          <sui-dropdown
            placeholder="Select target grade"
            @input="calculate(); log();"
            :options="this.grade_collection"
            selection
            search
            v-model="target_grade"
          />
        </sui-form-field>
        <br>
        <!--<button type="button" class="btn btn-create" @click="removeDupStudentToAssignment()">Add/Update Grade</button>-->
      </sui-form>

      <!-- Standing -->
      <h2 class="alignleft">Standing</h2>
      <sui-table celled >
        <sui-table-header>
        <sui-table-row>
          <sui-table-header-cell :width="2"></sui-table-header-cell>
          <sui-table-header-cell :width="2">Mastered</sui-table-header-cell>
          <sui-table-header-cell :width="2">Competency</sui-table-header-cell> 
        </sui-table-row>
        </sui-table-header>
        <sui-table-body>        
        <sui-table-row>
          <sui-table-cell>Current ({{letterGrade}})</sui-table-cell>
          <sui-table-cell>{{ numNodesMast }}</sui-table-cell>
          <sui-table-cell>{{ numNodesComp }}</sui-table-cell>
        </sui-table-row>
        <sui-table-row>
          <sui-table-cell>Target ({{this.gradeToLetter(target_grade)}})</sui-table-cell>
          <sui-table-cell> {{ target_mastered }} </sui-table-cell>
          <sui-table-cell> {{ target_comp }} </sui-table-cell>
        </sui-table-row>
        </sui-table-body>
      </sui-table>

      <!-- Plan -->
      <h2 class="alignleft">Plan</h2>
      <sui-table celled >
        <sui-table-header>
        <sui-table-row>
          <sui-table-header-cell :width="2"></sui-table-header-cell>
          <sui-table-header-cell :width="2">Mastered</sui-table-header-cell>
          <sui-table-header-cell :width="2">Competency</sui-table-header-cell> 
        </sui-table-row>
        </sui-table-header>
        <sui-table-body>        
        <sui-table-row>
          <sui-table-cell>Current ({{letterGrade}})</sui-table-cell>
          <sui-table-cell>{{ numNodesMast }}</sui-table-cell>
          <sui-table-cell>{{ numNodesComp }}</sui-table-cell>
        </sui-table-row>
        </sui-table-body>  
      </sui-table>
    </div>
    <h2 v-else>
      Failed to get grade data
    </h2>

  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapMutations } from 'vuex';
import { API_URL } from '@/constants';

export default {
  components: {
    
  },
  props: {
    role: {
      type: String,
      default: 'professor',
    },
    data: {
      type: Object,
    },
    id: {
      type: String,
      required: true,
    },
    letterGrade: {
      type: String,
      required: true,
    }, 
    numNodesComp: { // TODO: Refactor - These may not all be needed. Maybe can be made smaller
      type: Number,
      required: true,
    },
    numNodesMast: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      competency_thresholds: {},
      grade_thresholds: {},

      target_grade: '',
      target_mastered: '?',
      target_comp: '?',
      grade_collection: [],
      letters: ['A','B','C','D'],
      additions: ['+','','-']
    };
  },
  mounted() {
    this.retrieveResources();
    this.setGrades();
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    // TODO: Refactor this and include is as a prop rather than 
    retrieveResources() {
      const profile = JSON.parse(localStorage.getItem('profile'));
      axios.get(`${API_URL}/courses/${this.id}/competency-threshold`, { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } })
        .then((comp) => {
          this.competency_thresholds = comp.data.result;
          delete this.competency_thresholds.pk;
          delete this.competency_thresholds.course;
        });
      axios.get(`${API_URL}/courses/${this.id}/grade-threshold`, { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } })
        .then((grade) => {
          this.grade_thresholds = grade.data.result;
          delete this.grade_thresholds.pk;
          delete this.grade_thresholds.course;
        });
    },
    addToStr(add) {
      if (add === '+')
        return '_plus';
      if (add === '-')
        return '_minus';
      return '';
    },
    strToAdd(str) {
      if (str === 'plus')
        return '+';
      if (str === 'minus')
        return '-';
      return '';
    },
    gradeToLetter(grade) {
      let temp = grade.split('_');
      let ret = '';
      if (temp.length > 0)
        ret += temp[0].toUpperCase();
      if (temp.length > 1)
        ret += this.strToAdd(temp[1]);
      return ret;
    },
    setGrades() {
      this.letters.forEach(letter => {
        this.additions.forEach(add => {
          this.grade_collection.push({value:letter.toLowerCase()+this.addToStr(add),text:letter+add});
        });
      });
    },
    calculate() {
      this.target_mastered = this.grade_thresholds[this.target_grade+'_mastery'];
      this.target_comp = this.grade_thresholds[this.target_grade+'_competency'];
    },
    log() {
      console.log(this.target_grade + ' ' + this.target_mastered + ' ' + this.target_comp);

    },
    
  }
};

</script>

<style scoped>
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
    -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34,36,38,.15);
    box-shadow: 0 0.75pt 1.5pt 0 rgba(34,36,38,.15);
    border: 0.75pt solid rgba(34,36,38,.15);
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

  .selected {
    background-color:lightgreen;
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