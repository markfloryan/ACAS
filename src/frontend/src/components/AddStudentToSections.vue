<template>
  <div class="section-modal" @click.self="closeModal()">
    <div class="content">
      <h1 style="border-bottom: solid 0.75pt lightgray; padding-bottom: 8pt;">Add {{ name }} to sections</h1>
      <sui-form @submit.prevent>
        <label>Sections</label>
        <sui-form-field>
          <sui-dropdown
            multiple
            fluid
            :options="sections"
            placeholder="Sections"
            search
            selection
            v-model="selections"
          />
        </sui-form-field>
        <div style="text-align: center;">
          <button type="button" @click="closeModal()" style="margin-right: 8pt;" class="btn btn-plain cancel-btn">Cancel</button>
          <button type="button" @click="updateStudent()" class="btn btn-create create-btn">Update</button>
        </div>
      </sui-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';

export default {
  name: 'EditSection',
  components: {
    
  },
  props: {
    prefill: {
      type: Object,
      required: false,
    },
    course: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      name: '',
      student_id: 0,
      sectionsStudentIsIn: [],
      sections: [],
      selections: [],
    };
  },
  mounted() {
    console.log(this.prefill);
    if(this.prefill != null) {
      this.name = this.prefill.name;
      this.student_id = this.prefill.value;
    }

    this.prefill.sections.forEach(section => {
      this.sectionsStudentIsIn.push(section.id);
    });
    this.getSections();
  },
  created() {
    // console.log(this.data);
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    closeModal() {
      this.$emit('onClose');
    },
    getSections() {
      axios
        .get(`${API_URL}/sections/?courseId=${this.course}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
        .then(response => {
          if(response.status == 200) {
            let temparr = [];
            response.data.result.forEach(section => {
              temparr.push({text: `${section.name} - ${section.section_code}`, value: section.pk});
              if(this.sectionsStudentIsIn.includes(section.pk)) {
                this.selections.push(section.pk);
              }
            });
            this.sections = temparr;
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    updateStudent() {
      let success = true;
      this.sectionsStudentIsIn.forEach(section => {

        if(!this.selections.includes(section)) {
          axios
            .delete(`${API_URL}/student/section/?sectionId=${section}&studentId=${this.student_id}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
            .then(response => {
            })
            .catch(error => {
              console.log(error);
              success = false;
            });
        }
      });

      this.selections.forEach(section => {
        if(!this.sectionsStudentIsIn.includes(section)) {
          let data = {
            student: this.student_id,
            section: section,
          };

          axios
            .post(`${API_URL}/student/section/`, data, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
            .then(response => {
            })
            .catch(error => {
              console.log(error);
              success = false;
            });
        }
      });

      if (success) {
        this.openToast();
        this.setToastInfo({
          type: 'success',
          title: 'Successful Update',
          message: 'Student sections successfully updated',
          duration: 5000,
        });
      } else {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Failed Update',
          message: 'Something went wrong...',
          duration: 5000,
        });
      }

      this.closeModal();
    }
  }
};
</script>

<style scoped>
  .section-modal {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1000000;
    width: 100%;
    height: 100%;
    background-color: rgba(100, 100, 100, 0.8);
  }
  .section-modal > .content {
    grid-area: content;
    background-color: #fff;
    -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34,36,38,.15);
    box-shadow: 0 0.75pt 1.5pt 0 rgba(34,36,38,.15);
    border: 0.75pt solid rgba(34,36,38,.15);
    padding: 8pt;
    border-radius: 6pt;
    
    margin: auto;
    width: 300pt;
    min-width: 225pt;
    height: min-content;
    position: relative;
    top: 50%;
    transform: perspective(0.75pt) translateY(-50%);
    padding: 18pt;
  }
  .section-modal > .content > .title {
    grid-area: title;
  }
  .section-modal > .content > .tab-nav {
    grid-area: tabnav;
  }
  .section-modal > .content > .main {
    grid-area: main;
  }
  .section-modal-button {
    cursor: pointer;
    grid-area: exit;
  }
  .section-modal-button:hover {
    color: var(--color-blue);
  }
</style>