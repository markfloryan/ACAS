<!-- View for students to see course grading policy -->
<template>
  <div class="main">
    
    <div v-if="true" style="margin-top: 8pt; overflow-y: scroll">
      <div>
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
                <sui-table-cell>Current Grade ({{letterGrade}})</sui-table-cell>
                <sui-table-cell>{{ numNodesMast }}</sui-table-cell>
                <sui-table-cell>{{ numNodesComp }}</sui-table-cell>
            </sui-table-row>
            <sui-table-row>
                <!-- 
                    TODO: Post next grade
                    Layout looks pretty janky too. Better way?
                -->
                <sui-table-cell>Next Grade</sui-table-cell>
                <sui-table-cell> ? </sui-table-cell>
                <sui-table-cell> ? </sui-table-cell>
            </sui-table-row>
            </sui-table-body>
        </sui-table>
      </div>
      <br>
      <!-- Display competency threshold info -->
      <div v-if="Object.keys(competency_thresholds).length > 0">
        <h2 class="alignleft">Competency Thresholds</h2>
        <sui-table celled >
            <sui-table-header>
            <sui-table-row>
                <sui-table-header-cell :width="2">Mastered</sui-table-header-cell>
                <sui-table-header-cell :width="2">Competency</sui-table-header-cell>
            </sui-table-row>
            </sui-table-header>
            <sui-table-body>        
            <sui-table-row v-for="index in 1" :key="`${index}`" :set="vals = Object.values(competency_thresholds)">
                <sui-table-cell>{{ vals[1] }}</sui-table-cell>
                <sui-table-cell>{{ vals[0] }}</sui-table-cell>
            </sui-table-row>
            </sui-table-body>
        </sui-table>
      </div>
      <br>
      <!-- Display grade threshold info -->
      <div v-if="Object.keys(grade_thresholds).length > 0">
        <div>
            <h2 class="alignleft">Grading Thresholds</h2>
            <h3 class="alignright">(# mastered / # competency)</h3>
        </div>
        <sui-table celled >
            <sui-table-header>
            <sui-table-row>
                <sui-table-header-cell :width="2"></sui-table-header-cell>
                <sui-table-header-cell :width="2">+</sui-table-header-cell>
                <sui-table-header-cell :width="2">=</sui-table-header-cell>
                <sui-table-header-cell :width="2">-</sui-table-header-cell>
            </sui-table-row>
            </sui-table-header>
            <sui-table-body>        
            <sui-table-row v-for="index in 4" :key="`${index}`" :set="vals = Object.values(grade_thresholds)" :temp="i = index*6">
                <sui-table-cell>{{ letters[index-1]}}</sui-table-cell>
                <!-- Display master / competency requirements and highlights the current grade -->
                <sui-table-cell v-bind:class="{ selected: index-1 == letter_pos && addition_pos == 0 }">{{ vals[i-6] + ' / ' + vals[i-5]}}</sui-table-cell>
                <sui-table-cell v-bind:class="{ selected: index-1 == letter_pos && addition_pos == 1 }">{{ vals[i-4] + ' / ' + vals[i-3]}}</sui-table-cell>
                <sui-table-cell v-bind:class="{ selected: index-1 == letter_pos && addition_pos == 2 }">{{ vals[i-2] + ' / ' + vals[i-1]}}</sui-table-cell>
            </sui-table-row>
            </sui-table-body>
        </sui-table>
      </div>
    </div>
    <h2 v-else>
      Failed to get grade thresholds
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
      letters: ['A','B','C','D'],
      letter_pos: '-1',
      addition_pos: '1',
    };
  },
  mounted() {
    this.retrieveResources();
    this.setGradeHighlightIndex();
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    retrieveResources() {
      const profile = JSON.parse(localStorage.getItem('profile'));
      axios.get(`${API_URL}/courses/${this.id}/competency-threshold`, { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } })
        .then((comp) => {
          this.competency_thresholds = comp.data.result;
          this.competency_thresholds['course'] = {}; // This can probably be removed
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
    setGradeHighlightIndex() {
      if (this.letterGrade.length > 1) {
        if (this.letterGrade.substring(1) === '+')
          this.addition_pos = 0;
        else
          this.addition_pos = 2;
      }

      for (var i = 0; i < this.letters.length; i++) {
        if (this.letterGrade.substring(0,1) == this.letters[i])
          this.letter_pos = i;
      }
        
    }   
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