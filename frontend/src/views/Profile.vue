<template>
  <div class="container-float">
    <div v-if="profile">
      <div class="mt-2">
        <div class="row">
          <div class="col-auto">
            <Avatar :image="profile.avatar" class="mr-2" size="large" shape="circle"/>
          </div>
          <div class="col-6">
            <FileUpload name="avatar"
                        :url="profile.avatar"
                        mode="basic"
                        accept="image/png,image/jpeg"
                        chooseLabel="Обновить"
                        auto
                        :multiple="false"
                        :maxFileSize="2000000"
                        invalidFileSizeMessage="Файл слишком большой. Размер файла должен быть меньше 2MB."
                        invalidFileTypeMessage="Неверный тип файла. Разрешены только изображения (PNG, JPEG)."
                        @upload="onUpload"
                        @error="onError"
                        :customUpload="true"
                        @uploader="uploadAvatar">
              <template #empty>
                <p>Drag and drop files to here to upload.</p>
              </template>
            </FileUpload>
          </div>
        </div>
      </div>
      <div class="mt-2">
        <label for="fio">Firstname</label>
        <InputText id="fio"
                   v-model="profile.firstname"
                   @blur="handleBlur('firstname')"
                   :disabled="isFormDisabled"
                   class="input-form"
                   :invalid="false"
                   inputmode="text"
                   label="Firstname"
                   placeholder="Firstname"
                   maxlength="100"
        />
        <small v-if="erroredProfile.firstname" class="error-message">{{ erroredProfile.firstname }}</small>
      </div>
      <div class="mt-2">
        <label for="fio">Lastname</label>
        <InputText id="fio"
                   v-model="profile.lastname"
                   @blur="handleBlur('lastname')"
                   :disabled="isFormDisabled"
                   class="input-form"
                   :invalid="false"
                   inputmode="text"
                   label="Lastname"
                   placeholder="Lastname"
                   maxlength="100"
        />
        <small v-if="erroredProfile.lastname" class="error-message">{{ erroredProfile.lastname }}</small>
      </div>
      <div class="mt-2">
        <label for="phone">Телефон</label>
        <InputText id="phone"
                   v-model="profile.user.phone"
                   :disabled="isFormDisabled"
                   class="input-form"
                   readonly
                   inputmode="tel"
                   label="ФИО"
                   placeholder="Телефон"
                   maxlength="15"
        />
      </div>
      <div class="mt-2">
        <label for="tg-login">Логин в телеграм</label>
        <InputText id="tg-login"
                   v-model="profile.user.tg_login"
                   :disabled="isFormDisabled"
                   class="input-form"
                   readonly
                   inputmode="tel"
                   label="Логин"
                   placeholder="Логин"
                   maxlength="15"
        />
      </div>
      <div class="mt-2">
        <label for="nickname">Никнейм</label>
        <InputText v-model="profile.nickname"
                   @blur="handleBlur('nickname')"
                   :disabled="isFormDisabled"
                   id="nickname"
                   class="input-form"
                   inputmode="text"
                   placeholder="Никнейм"
                   maxlength="50"
        />
        <small v-if="erroredProfile.nickname" class="error-message">{{ erroredProfile.nickname }}</small>
      </div>
      <div class="mt-2">
        <label for="birthdate">День рождения</label>
        <DatePicker v-model="profile.birthdate"
                    @blur="handleBlur('birthdate')"
                    :disabled="isFormDisabled"
                    id="birthdate"
                    touchUI
                    showIcon
                    class="input-form"
                    inputmode="text"
                    date-format="yy-mm-dd"
        />
        <small v-if="erroredProfile.birthdate" class="error-message">{{ erroredProfile.birthdate }}</small>
      </div>
      <div class="mt-2">
        <label for="social">Соц. сети</label>
        <Textarea v-model="profile.social"
                  @blur="handleBlur('social')"
                  :disabled="isFormDisabled"
                  id="social"
                  class="input-form"
                  inputmode="text"
                  placeholder="Соц. сети"
                  rows="4"
                  cols="30" maxlength="100"
        />
        <small v-if="erroredProfile.social" class="error-message">{{ erroredProfile.social}}</small>
      </div>
    </div>
    <div v-else>
      <!-- Skeleton for avatar -->
      <div class="mt-2">
        <div class="row">
          <div class="col-auto">
            <Skeleton shape="circle" size="3rem" class="mr-2"></Skeleton>
          </div>
          <div class="col-6">
            <Skeleton width="8rem" height="3.5rem" class="mb-2"></Skeleton>
          </div>
        </div>
      </div>
      <!-- Skeleton for firstname -->
      <div class="mt-2">
        <label for="fio">Firstname</label>
        <Skeleton width="100%" height="2rem" class="mb-2"></Skeleton>
      </div>
      <!-- Skeleton for lastname -->
      <div class="mt-2">
        <label for="fio">Lastname</label>
        <Skeleton width="100%" height="2rem" class="mb-2"></Skeleton>
      </div>
      <!-- Skeleton for Телефон -->
      <div class="mt-2">
        <label for="phone">Phone</label>
        <Skeleton width="100%" height="2rem" class="mb-2"></Skeleton>
      </div>
      <!-- Skeleton for Логин в телеграм -->
      <div class="mt-2">
        <label for="tg-login">Логин в телеграм</label>
        <Skeleton width="100%" height="2rem" class="mb-2"></Skeleton>
      </div>
      <!-- Skeleton for Никнейм -->
      <div class="mt-2">
        <label for="nickname">Никнейм</label>
        <Skeleton width="100%" height="2rem" class="mb-2"></Skeleton>
      </div>
      <!-- Skeleton for День рождения -->
      <div class="mt-2">
        <label for="birthdate">День рождения</label>
        <Skeleton width="100%" height="2rem" class="mb-2"></Skeleton>
      </div>
      <!-- Skeleton for Соц. сети -->
      <div class="mt-2">
        <label for="social">Соц. сети</label>
        <Skeleton width="100%" height="6rem" class="mb-2"></Skeleton>
      </div>
    </div>
    <Toast :breakpoints="{'420px': { width: '75vw'}}" position="bottom-center"/>
  </div>
</template>

<script>
import {inject, onMounted, ref} from 'vue';
import axiosInstance from "@/axios.js";
import {API_URL_PROFILE_ME} from "@/constants/ada-api.js";
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import {useToast} from "primevue/usetoast";
import {useStore} from "vuex";

export default {
  name: 'Profile',
  components: {
    InputText,
    Button,
  },
  setup() {
    const profile = ref(null);
    const originalProfile = ref(null);
    const erroredProfile = ref({});
    const erroredProfileValues = ref({});
    const changedFields = ref({});
    const globalState = inject('globalState');
    const store = useStore();
    const toast = useToast();
    const TWA = inject('TWA');
    const isFormDisabled = ref(false);

    const show = () => {

    }

    const fetchProfile = async () => {
      try {
        const response = await axiosInstance.get(API_URL_PROFILE_ME);
        profile.value = response.data;
        originalProfile.value = JSON.parse(JSON.stringify(response.data));
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Ошибка при загрузке профиля',
          detail: error.detail,
          life: 1500,
        })
      }
    };

    const updateProfile = async (fieldsToUpdate, isFileUpload = false) => {
      try {
        isFormDisabled.value = true;

        let headers = {};

        // Check if the update is for a file upload
        if (isFileUpload) {
          headers['Content-Type'] = 'multipart/form-data';
        } else {
          if (fieldsToUpdate.birthdate) {
            const date = new Date(fieldsToUpdate.birthdate);
            fieldsToUpdate.birthdate = date.getFullYear() + '-' +
                ('0' + (date.getMonth() + 1)).slice(-2) + '-' +
                ('0' + date.getDate()).slice(-2);
          }
        }


        const response = await axiosInstance.patch(API_URL_PROFILE_ME, fieldsToUpdate, {headers});
        await store.dispatch('auth/fetchUser', {TWA});

        toast.add({
          severity: 'success',
          summary: 'Успешно',
          detail: `Обновили ${response.data.modified.join(', ')}`,
          life: 5000,
        })

        response.data.modified.forEach(field => delete erroredProfile.value[field]);
        response.data.modified.forEach(field => delete erroredProfileValues.value[field]);

        Object.assign(originalProfile.value, fieldsToUpdate);
      } catch (error) {
        console.log('error response', error.response)
        let errorMessage = 'Неизвестная ошибка';
        if (error.response && error.response.data) {
          if (error.response.data.detail) {
            errorMessage = error.response.data.detail;
          } else if (typeof error.response.data === 'object' && Object.keys(error.response.data).length > 0) {
            Object.entries(error.response.data).forEach(([key, value]) => {
              erroredProfile.value[key] = value.join(", ");
            });
            errorMessage = Object.keys(error.response.data)
                .map(key => `${error.response.data[key].join(' ')}`)
                .join(', ');
          } else {
            try {
              errorMessage = JSON.stringify(error.response.data);
            } catch (e) {
              // If parsing fails, keep the default error message
            }
          }
        } else if (error.message) {
          errorMessage = error.message;
        }

        toast.add({
          severity: 'error',
          summary: 'Ошибка при обновлении профиля',
          detail: errorMessage,
          life: 5000,
        });
      }
      isFormDisabled.value = false;
    };

    const handleBlur = async (fieldName) => {
      const fieldOriginal = originalProfile.value[fieldName];
      const erroredField = erroredProfileValues.value[fieldName];
      const fieldCurrent = profile.value[fieldName];
      console.log(fieldOriginal, erroredField, fieldCurrent)
      if (JSON.stringify(fieldCurrent) !== JSON.stringify(fieldOriginal) && JSON.stringify(fieldCurrent) !== JSON.stringify(erroredField)) {
        changedFields.value[fieldName] = fieldCurrent;
        erroredProfileValues.value[fieldName] = fieldCurrent;  // Сохраняем новое значение в ошибку. Если не очистится из
                                                         // updateProfile (произошла ошибка) в следующий
                                                         // раз проигнорируется.
        await updateProfile(changedFields.value);
        changedFields.value = {};
      }
    };

    const uploadAvatar = async (event) => {
      const formData = new FormData();
      formData.append('avatar', event.files[0]);
      try {
        const response = await axiosInstance.patch(API_URL_PROFILE_ME, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Custom upload successful', response.data);
        await fetchProfile();
        // Update local profile data with new avatar URL if needed
      } catch (error) {
        console.error('Custom upload failed', error);
      }
    };

    // const handleAvatarChange = (event) => {
    //   const file = event.target.files[0];
    //   if (file) {
    //     const formData = new FormData();
    //     formData.append('avatar', file);
    //     updateProfile(formData, true);
    //   }
    // };

    const onUpload = (event) => {
      // Handle successful upload
      console.log('Upload successful', event);
    };

    const onError = (error) => {
      // Handle upload error
      console.log('Upload error', error);
    };

    onMounted(async () => {
      globalState.title = 'Профиль';
      // await new Promise(r => setTimeout(r, 500));

      await fetchProfile();
    });

    return {
      profile,
      updateProfile,
      erroredProfile,
      show,
      isFormDisabled,
      handleBlur,
      uploadAvatar,
      onUpload,
      onError,
    };
  },
};
</script>

<style scoped>
label {
  margin-left: 8px;
  font-weight: 500;
}

.profile-container {
  max-width: 384px;
  margin: auto;
  padding: 20px;
}

.input-form {
  width: 100%;
}

.error-message {
  color: #ff5252; /* Red text */
  font-size: 0.875em; /* Slightly smaller text */
}
</style>
