<script>
import { upload } from './service/fileUploadService'
import { download } from './service/downloadFileService'
import { wait } from './utils/wait'
import FileComponentVue from './components/FileComponent.vue';
import DownloadButtonComponentVue from './components/DownloadButtonComponent.vue';

const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3, EMPTY=true;

export default {
  components: {
    FileComponentVue,
    DownloadButtonComponentVue,
  },
  data() {
    return {
      filename: 'Clique e selecione o arquivo (.xls)',
      currentStatus: null,
      empty: true,
      blob: null,
    }
  },
  computed: {
    isInitial() {
      return this.currentStatus === STATUS_INITIAL;
    },
    isSaving() {
      return this.currentStatus === STATUS_SAVING;
    },
    isSuccess() {
      return this.currentStatus === STATUS_SUCCESS;
    },
    isFailed() {
      return this.currentStatus === STATUS_FAILED;
    },
    isEmpty() {
      return this.empty === EMPTY;
    }
  },
  methods: {
    setTag(tag) {
      this.tag = tag;
    },
    setFilename(filename) {
      this.filename = filename;
    },
    onChangeFile(event) {
      const filename = event.target.files.item(0).name;
      const fileList = event.target.files;

      this.setFilename(filename)
      
      const formData = new FormData();

      if (!fileList.length) return;

      Array
        .from(Array(fileList.length).keys())
        .map(item => {
          formData.append('file', fileList[item], fileList[item].name);
        });

      this.save(formData)
    },
    onChangeInput(event) {
      const tag = event.target.value;
      
      this.setTag(tag);

      if (tag !== '' || tag !== null) {
        this.empty = false;
      } else {
        this.empty = true;
      }
    },
    save(formData, query) { 
      this.currentStatus = STATUS_SAVING;

      upload(formData)
        .then(result => {
          this.currentStatus = STATUS_SUCCESS;
          this.blob = result.data;
          return result;
        })
        .catch(err => {
          this.currentStatus = STATUS_FAILED;
          return err;
        });
    },
    downloadFile() {
      download(this.blob);
    }
  }
}
</script>

<template>
  <header>
    <img src="/assets/logo.png" height="20" alt="Logo Padtec">
  </header>
  <div class="welcome-text">
    <img src="/assets/welcome-illustration.svg" height="275" alt="Welcome to PadUtil">
    <span class="text">
      Seja bem-vindo ao PadUtil para leitura do inventário de placas 
    </span>
    <div class="inventory-container">
      <FileComponentVue  
        :filename="filename" 
        :changeMethod="onChangeFile" 
        :accept="`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel`" 
        :class="`board-inventory-btn`"
        :name="`inventory`"
        :id="`board-inventory`"  
      />
      
      <img src="/assets/success-icon.svg" class="status-icon" alt="Upload feito com sucesso" v-if="isSuccess">
      <img src="/assets/failed-icon.svg" class="status-icon" alt="Upload falhou" v-if="isFailed">
      <img src="/assets/loading.svg" class="status-icon" alt="Carregando" v-if="isSaving">

    </div>
    
    <span v-if="isSuccess"><b>Resultado:</b></span>
    <DownloadButtonComponentVue
      :title="filename + `_RESULT`"
      :class="`result-btn`"
      :clickMethod="downloadFile"
      v-if="isSuccess"
    />

    <div class="err-message-container">
      <img src="/assets/warn-icon.svg" class="status-icon" alt="Upload falhou" v-if="isFailed">
      <span class="err-message" v-if="isFailed">
        Erro ao fazer o upload do arquivo! Tente novamente mais tarde
      </span>
    </div>
  </div>
</template>

<style>
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 75px;
  padding: 20px;
  box-shadow: 0px 0px 10px var(--color-shadow-background);
}

input[type="file"] {
  display: none;
}

.inventory-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.status-icon {
  padding-left: 10px;
}

.board-inventory-icon {
  padding-right: 10px;
}

.board-inventory-btn, .result-btn {
  display: flex;
  align-items: center;
  padding: 5px 45px;
  max-width: 400px;
  width: 100%;
  background-color: var(--principal-bg-color);
  color: var(--vt-c-white);
  text-align: center;
  margin-top: 10px;
  cursor: pointer;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
}

.result-btn {
  border: none;
}

.welcome-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 10px;
}

.welcome-text img {
  margin: 15px 0 ;
}

.welcome-text .text {
  max-width: 365px;
  width: 100%;
  text-align: center;
  font-weight: 600;
  font-size: 18px;
  margin-bottom: 15px;
}

.err-message-container {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: center;
}

.err-message {
  font-size: 12px;
  font-weight: 500;
  color: var(--error-color);
  padding: 10px;
  max-width: 372px;
  width: 100%;
  text-align: left;
}
</style>
