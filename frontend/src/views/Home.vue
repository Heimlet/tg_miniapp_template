<template>
  <div class="container-float">
    <div class="row mt-3">
      <PanelMenu :model="items" class="w-full md:w-15rem ada-panelmenu">
        <template #item="{ item }">
          <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
            <a v-ripple class="flex align-items-center cursor-pointer text-color px-3 py-2" :href="href"
               @click="navigate">
              <span :class="item.icon"></span>
              <span class="ml-2 text-color cursor-pointer">{{ item.label }}</span>
            </a>
          </router-link>
          <a v-else v-ripple class="flex align-items-center cursor-pointer text-color px-3 py-2" :href="item.url"
             :target="item.target">
            <span :class="item.icon"></span>
            <span class="ml-2">{{ item.label }}</span>
            <span v-if="item.items" class="pi pi-angle-down cursor-pointer text-primary ml-auto"></span>
          </a>
        </template>
      </PanelMenu>
    </div>
    <Toast :breakpoints="{'420px': { width: '75vw' }}" position="bottom-top"/>
  </div>
</template>

<script>
import {computed, inject, onMounted, ref, watchEffect} from 'vue';
import {useStore} from 'vuex';
import {useRouter} from 'vue-router';
import {useToast} from 'primevue/usetoast';

export default {
  name: 'Home',
  setup() {
    const store = useStore();
    const toast = useToast();
    const globalState = inject('globalState');
    const TWA = inject('TWA');
    const router = useRouter();
    const items = ref([]);

    const user = computed(() => store.getters['auth/user']);

    const updateMenuItems = () => {
      items.value = [
        {
          label: 'Report',
          icon: 'pi pi-file-excel',
          items: [
            {
              label: 'My payments',
              icon: 'pi pi-bitcoin',
              command: () => {
                toast.add({
                  severity: 'warn',
                  summary: 'Warning',
                  detail: 'Section is under development!',
                  life: 2500,
                });
              },
            },
            {
              label: 'My data',
              icon: 'pi pi-credit-card',
              command: () => {
                toast.add({
                  severity: 'warn',
                  summary: 'Warning',
                  detail: 'Section is under development!',
                  life: 2500,
                });
              },
            },
          ]
        },
        {
          label: 'About us',
          icon: 'pi pi-info',
          command: () => {
            toast.add({
              severity: 'warn',
              summary: 'Warning',
              detail: 'Section is under development!',
              life: 2500,
            });
          },
        },
        {
          label: 'Our Events',
          icon: 'pi pi-book',
          command: () => {
            toast.add({
              severity: 'warn',
              summary: 'Warning',
              detail: 'Section is under development!',
              life: 2500,
            });
          },
        },
        {
          label: 'Support',
          icon: 'pi pi-heart-fill',
          command: () => {
            toast.add({
              severity: 'warn',
              summary: 'Warning',
              detail: 'Section is under development!',
              life: 2500,
            });
          },
        },
      ].filter(Boolean);
    };

    const goToProfilePage = () => {
      router.push({name: 'Profile'});
    };

    watchEffect(() => {
      updateMenuItems();
    });
    onMounted(async () => {
      globalState.title = 'Menu';
      TWA.BackButton.hide();
      updateMenuItems();
    });

    return {
      goToProfilePage,
      user,
      items,
    };
  },
};
</script>

<style lang="scss">
.container-float {
  padding: 1rem;
}

.ada-panelmenu {
  .p-panelmenu-header-content {
    padding: 0.3rem;
  }

  .p-menuitem-content {
    padding: 0.3rem;
  }

  .p-panelmenu-item {
    .p-panelmenu-item-content {
      padding: 0.5rem;
    }
  }

}

.ml-2 {
  margin-left: 0.5rem;
}
</style>