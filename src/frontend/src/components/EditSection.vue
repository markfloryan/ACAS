<template>
  <div class="section-modal" @click.self="closeModal()">
    <div class="content">
      <h1 v-if="create" style="border-bottom: solid 0.75pt lightgray; padding-bottom: 8pt;">Create a new section:</h1>
      <h1 v-if="!create" style="border-bottom: solid 0.75pt lightgray; padding-bottom: 8pt;">Edit this section:</h1>
      <sui-form @submit.prevent>
        <sui-form-field>
          <label>Section name</label>
          <input v-model="sname" placeholder="Section name" type="text">
        </sui-form-field>
        <sui-form-field>
          <label>Section code</label>
          <input v-model="scode" placeholder="Section code" type="text">
        </sui-form-field>
        <div style="text-align: center;">
          <button type="button" @click="closeModal()" style="margin-right: 8pt;" class="btn btn-plain cancel-btn">Cancel</button>
          <button v-if="create" type="button" @click="createSection()" class="btn btn-create create-btn">Create</button>
          <button v-if="!create" type="button" @click="updateSection()" class="btn btn-create create-btn">Update</button>
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
    create: {
      type: Boolean,
      required: true,
    },
    course: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      sname: '',
      scode: '',
    };
  },
  mounted() {
    if(this.prefill != null) {
      this.sname = this.prefill.name;
      this.scode = this.prefill.section_code;
    }
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
    createSection() {
      let sectionData = {
        course: this.course,
        name: this.sname,
        section_code: this.scode,
      };

      axios
        .post(`${API_URL}/sections/`, sectionData, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
        .then(response => {
          if(response.status == 200) {
            this.openToast();
            this.setToastInfo({
              type: 'success',
              title: 'Successful Creation',
              message: 'Section successfully created',
              duration: 5000,
            });
            this.closeModal();
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    updateSection() {
      let sectionData = {
        course: this.course,
        name: this.sname,
        section_code: this.scode,
      };

      axios
        .put(`${API_URL}/sections/${this.prefill.pk}`, sectionData, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
        .then(response => {
          if(response.status == 200) {
            this.openToast();
            this.setToastInfo({
              type: 'success',
              title: 'Successful Update',
              message: 'Section successfully updated',
              duration: 5000,
            });
            this.closeModal();
          }
        })
        .catch(error => {
          console.log(error);
        });
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