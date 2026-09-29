/**
 * ИНДУСТРИАЛЬНЫЙ АТЛАС КУРСКОЙ ОБЛАСТИ // КЭМТ & IT-ЦОПП
 * Interactive Engine: Optical Loupe Splitter, Parallax, Bento Filters, HUD Modals, Career Quiz
 */

(function () {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  // --- DATASET: 11 ВОСТРЕБОВАННЫХ ПРОФЕССИЙ КУРСКОЙ ОБЛАСТИ ---
  const PROFESSIONS_DATA = {
    "welding": {
      num: "01",
      title: "Сварщик (электрогазосварщик, TIG/MIG)",
      category: "metal",
      categoryName: "Металлообработка",
      demand: 98,
      salary: "85 000 — 185 000 ₽",
      icon: "welding",
      shortDesc: "Ручная аргонодуговая сварка неплавящимся электродом (TIG) и механизированная сварка (MIG/MAG) корпусных конструкций, сосудов под давлением и трубопроводов 1–2 контуров Курской АЭС-2.",
      specs: {
        equipment: "Инверторные сварочные аппараты Lincoln Electric, Miller, Кедр; защитный газ — высший сорт аргона ГОСТ 10157-2016.",
        materials: "Высоколегированные коррозионностойкие аустенитные стали 08Х18Н10Т, перлитные теплоустойчивые стали 15Х2НМФА.",
        standards: "НП-084-15 (Правила контроля сварных соединений оборудования АЭУ), ГОСТ Р ИСО 9606-1, РД 153-34.1-003-01."
      },
      qualification: {
        ranks: "4–6 квалификационный разряд, аттестация НАКС (Национальное Агентство Контроля Сварки) I–II уровень.",
        tolerances: "100% неразрушающий контроль: рентгенографический (РК), ультразвуковой (УЗК) и цветная дефектоскопия (ЦД). Допуск к работе на высоте.",
        shift: "Сменный график 2/2 или вахта на строительной площадке Курской АЭС-2; спецодежда 3-го класса защиты от искр и брызг."
      },
      career: {
        employers: ["Курская АЭС-2 (ГК Росатом)", "Михайловский ГОК им. А.В. Варичева", "АО «Электроагрегат»", "ООО «Курск-Спецсталь»"],
        growth: "Сварщик 4 разряда → Бригадир сварочно-монтажного участка → Инспектор сварочного производства → Главный сварщик предприятия.",
        colleges: ["ОБПОУ «КЭМТ»", "Курский политехнический колледж", "Железногорский политехнический колледж"]
      }
    },
    "cnc-operator": {
      num: "02",
      title: "Оператор-наладчик станков с ЧПУ",
      category: "metal",
      categoryName: "Металлообработка",
      demand: 96,
      salary: "90 000 — 175 000 ₽",
      icon: "cnc",
      shortDesc: "Наладка и высокоточная обработка деталей на 3- и 5-осевых фрезерных и токарных обрабатывающих центрах. Программирование стоек Fanuc, Siemens Sinumerik и Heidenhain.",
      specs: {
        equipment: "Обрабатывающие центры Fanuc Robodrill D21SiB5, DMG Mori, Haas VF-2; мерительный инструмент с ценой деления 0.001 мм.",
        materials: "Титановые сплавы ВТ6, инструментальные стали Х12МФ, жаропрочные никелевые сплавы ЭИ437Б, дюралюминий Д16Т.",
        standards: "ГОСТ 2.307-2011 (Нанесение размеров и допусков), квалитеты точности IT5–IT7, шероховатость Ra 0.4–0.8."
      },
      qualification: {
        ranks: "4–6 разряд, чтение сложных пространственных 3D-моделей и управляющих программ в G-кодах.",
        tolerances: "Допуск на биение шпинделя и погрешность позиционирования до ±0.003 мм. Допуск по электробезопасности II группа.",
        shift: "Сменный график 2/2 (день/ночь) в прецизионном термоконстантном цехе (+20°C ±1°C)."
      },
      career: {
        employers: ["КЭАЗ (Курский электроаппаратный завод)", "ОБПОУ «КЭМТ» Lab", "АО «Авиаавтоматика им. В.В. Тарасова»", "АО «Геомаш»"],
        growth: "Оператор станков с ЧПУ → Наладчик 6 разряда → Программист-технолог ЧПУ (CAM) → Начальник механообрабатывающего цеха.",
        colleges: ["ОБПОУ «Курский электромеханический техникум» (КЭМТ)", "Курский политехнический колледж"]
      }
    },
    "lathe": {
      num: "03",
      title: "Токарь (токарь-универсал 4–6 разряда)",
      category: "metal",
      categoryName: "Металлообработка",
      demand: 92,
      salary: "75 000 — 150 000 ₽",
      icon: "lathe",
      shortDesc: "Механическая токарная обработка сложных корпусных деталей, ступенчатых валов, нарезание нестандартных упорных и метрических резьб на универсальных и карусельных станках.",
      specs: {
        equipment: "Токарно-винторезные станки 16К20, 1М63 (Дип-300), токарно-карусельные станки 1512 для крупногабаритных поковок.",
        materials: "Конструкционные углеродистые стали ст45, 40ХН2МА, бронза БрАЖ9-4, латунь ЛС59-1.",
        standards: "ГОСТ 25346-89 (ЕСДП), ГОСТ 24705-2004 (Резьба метрическая)."
      },
      qualification: {
        ranks: "4–6 разряд, филигранное владение микрометрическими нутромерами, индикаторными стойками и калибрами.",
        tolerances: "Точность обработки посадочных шеек валов до 0.01 мм, допуск круглости и соосности.",
        shift: "Односменный или двухсменный график в инструментальных и ремонтно-механических цехах."
      },
      career: {
        employers: ["АО «Электроагрегат»", "КЭАЗ", "Михайловский ГОК им. Варичева (РМУ)", "ОАО «Курскрезинотехника»"],
        growth: "Токарь 3-4 разряда → Токарь высшего 6 разряда → Мастер инструментального участка → Технолог механообработки.",
        colleges: ["ОБПОУ «КЭМТ»", "Железногорский горно-металлургический колледж (ЖГМК)"]
      }
    },
    "repairman": {
      num: "04",
      title: "Слесарь-ремонтник промышленного оборудования",
      category: "heavy",
      categoryName: "Тяжелая промышленность",
      demand: 91,
      salary: "70 000 — 135 000 ₽",
      icon: "repair",
      shortDesc: "Диагностика, капитальный ремонт, регулировка и балансировка промышленного оборудования, мощных редукторов, дробильно-размольных комплексов и гидравлических станций МГОК.",
      specs: {
        equipment: "Лазерные системы центровки валов Easy-Laser, гидросъемники усилием до 50 тонн, вибродиагностические комплексы.",
        materials: "Высокопрочные подшипники SKF, FAG, полимерные гидравлические уплотнения, специализированные смазки Mobil Mobilgrease.",
        standards: "ГОСТ 28.001-83 (Система технического обслуживания и ремонта техники)."
      },
      qualification: {
        ranks: "4–6 разряд, стропальные работы, безопасное обслуживание гидроприводов высокого давления до 32 МПа.",
        tolerances: "Допуск соосности муфтовых соединений до 0.05 мм, контроль тепловых зазоров подшипников.",
        shift: "Сменный график дежурного слесаря или дневной ремонтный регламент."
      },
      career: {
        employers: ["ПАО «Михайловский ГОК им. А.В. Варичева»", "ООО «Курскхимволокно»", "КЭАЗ", "МУП «Курскводоканал»"],
        growth: "Слесарь-ремонтник → Механик отделения → Главный механик обогатительной фабрики.",
        colleges: ["Железногорский горно-металлургический колледж (ЖГМК)", "Курский политехнический колледж"]
      }
    },
    "electrician-repair": {
      num: "05",
      title: "Электромонтер по ремонту и обслуживанию электрооборудования",
      category: "power",
      categoryName: "Энергетика",
      demand: 94,
      salary: "65 000 — 140 000 ₽",
      icon: "electrician",
      shortDesc: "Обслуживание распределительных устройств 10/6/0.4 кВ, силовых трансформаторов, релейной защиты, частотно-регулируемых электроприводов и систем автоматизации.",
      specs: {
        equipment: "Тепловизоры Fluke, мегомметры до 2500В, трассоискатели, испытательные стенды высоковольтной изоляции.",
        materials: "Кабели с изоляцией из сшитого полиэтилена, вакуумные выключатели КЭАЗ OptiMat, микропроцессорные блоки РЗА.",
        standards: "ПУЭ (Правила устройства электроустановок 7-е изд.), ПТЭЭП, ГОСТ Р 50571."
      },
      qualification: {
        ranks: "4–6 разряд, III–IV группа допуска по электробезопасности до и выше 1000В с правом оперативных переключений.",
        tolerances: "Чтение принципиальных электрических схем, проверка сопротивления изоляции и заземляющих контуров.",
        shift: "Оперативный сменный график (12 часов) на заводских подстанциях и главных распределительных щитах."
      },
      career: {
        employers: ["Филиал ПАО «Россети Центр» - «Курскэнерго»", "Курская АЭС", "КЭАЗ", "Михайловский ГОК"],
        growth: "Электромонтер 4 разряда → Мастер смены → Инженер-энергетик → Главный энергетик предприятия.",
        colleges: ["ОБПОУ «КЭМТ»", "Курский политехнический колледж"]
      }
    },
    "electrician-install": {
      num: "06",
      title: "Электромонтажник (электрооборудования)",
      category: "power",
      categoryName: "Энергетика",
      demand: 89,
      salary: "75 000 — 160 000 ₽",
      icon: "cabling",
      shortDesc: "Монтаж силовых кабельных трасс, распределительных трансформаторных подстанций, сборка и расключение шкафов автоматики строящихся энергоблоков Курской АЭС-2.",
      specs: {
        equipment: "Гидравлические прессы для опрессовки наконечников КВТ, кабельные лебедки, лазерные нивелиры Hilti.",
        materials: "Огнестойкие кабели ВВГнг(А)-FRLS, кабельные лотки горячего цинкования, шинопроводы до 4000А.",
        standards: "СП 76.13330.2016 (Электротехнические устройства), ГОСТ 31565-2012."
      },
      qualification: {
        ranks: "3–5 разряд, III группа допуска до 1000В, допуск к работам на высоте и монтажу кабельных проходок.",
        tolerances: "Монтаж с сохранением радиусов изгиба тяжелых кабелей, фазировка цепей, проверка момента затяжки динамометром.",
        shift: "Строительный график 5/2 или вахта на площадке АЭС-2; полный комплект СИЗ."
      },
      career: {
        employers: ["АО «АСЭ» (Инжиниринговый дивизион Росатома)", "ООО «Курскэлектромонтаж»", "АО «Электросетьремонт»"],
        growth: "Электромонтажник → Бригадир монтажников → Начальник участка электромонтажных работ.",
        colleges: ["Курский монтажный техникум", "ОБПОУ «КЭМТ»"]
      }
    },
    "rebar": {
      num: "07",
      title: "Арматурщик",
      category: "construction",
      categoryName: "Строительство",
      demand: 88,
      salary: "70 000 — 145 000 ₽",
      icon: "rebar",
      shortDesc: "Изготовление и пространственная сборка тяжелых арматурных каркасов, предварительно напрягаемой арматуры для фундаментных плит и гермооболочек Курской АЭС-2.",
      specs: {
        equipment: "Станки для гибки и резки арматурной стали диаметром до 40 мм, пистолеты для автоматической вязки арматуры Max.",
        materials: "Горячекатаная арматурная сталь периодического профиля классов А500С, А600С ГОСТ 34028-2016.",
        standards: "СП 63.13330.2018 (Бетонные и железобетонные конструкции), ГОСТ 10922-2012."
      },
      qualification: {
        ranks: "3–5 разряд, чтение сложных чертежей КЖ (конструкции железобетонные), стропальные удостоверения.",
        tolerances: "Точность шага стержней каркаса до ±5 мм, соблюдение защитного слоя бетона фиксаторами.",
        shift: "Сменный режим на открытой строительной площадке; виброзащитные рукавицы и защитные каски."
      },
      career: {
        employers: ["МУСП «Курскстрой»", "ГК Титан-2 (Генеральный подрядчик АЭС-2)", "АО «Концерн Росэнергоатом»"],
        growth: "Арматурщик → Бригадир комплексной бригады → Мастер арматурного цеха → Прораб монолитных работ.",
        colleges: ["Курский монтажный техникум", "Курский государственный политехнический колледж"]
      }
    },
    "concrete": {
      num: "08",
      title: "Бетонщик",
      category: "construction",
      categoryName: "Строительство",
      demand: 85,
      salary: "65 000 — 130 000 ₽",
      icon: "concrete",
      shortDesc: "Укладка, вибрирование и уход за специальными гидротехническими и радиационно-стойкими тяжелыми бетонными смесями в защитные конструкции и фундаменты.",
      specs: {
        equipment: "Глубинные высокочастотные вибраторы Wacker Neuson, заглаживающие машины («вертолеты»), бетононасосы Putzmeister.",
        materials: "Самоуплотняющиеся высокопрочные бетоны классов В60–В80 с микрокремнеземом и пластификаторами последнего поколения.",
        standards: "ГОСТ 7473-2010 (Смеси бетонные), СП 70.13330.2012 (Несущие и ограждающие конструкции)."
      },
      qualification: {
        ranks: "3–5 разряд, контроль осадки конуса, температурного графика прогрева бетона в зимнее время.",
        tolerances: "Непрерывность бетонирования критических узлов реакторного здания, исключение холодных швов.",
        shift: "Круглосуточный цикл монолитного бетонирования по сменному графику."
      },
      career: {
        employers: ["Холдинг ТИТАН-2", "ООО «Курский завод КПД им. Дериглазова»", "АО «Атомстройэкспорт»"],
        growth: "Бетонщик → Мастер бетонных работ → Начальник БСУ (бетоносмесительного узла).",
        colleges: ["Курский монтажный техникум"]
      }
    },
    "installer": {
      num: "09",
      title: "Монтажник металлических и железобетонных конструкций",
      category: "construction",
      categoryName: "Строительство",
      demand: 90,
      salary: "80 000 — 165 000 ₽",
      icon: "installer",
      shortDesc: "Монтаж каркасов промышленных цехов, эстакад технологических трубопроводов, тяжелых стальных балок перекрытий и технологических модулей реакторного зала.",
      specs: {
        equipment: "Монтажные гидродомкраты, гайковерты с контролем крутящего момента Plarad, лазерные тахеометры Leica.",
        materials: "Прокатная сталь С345, высокопрочные болты ГОСТ Р 52644 с предварительным натяжением.",
        standards: "СП 16.13330.2017 (Стальные конструкции), ГОСТ 23118-2019."
      },
      qualification: {
        ranks: "4–6 разряд, аттестация на монтаж на высоте (3 группа безопасности), стропальщик 5 разряда.",
        tolerances: "Отклонение вертикальности колонн каркаса не более 5 мм на 30 метров высоты.",
        shift: "Строительный сменный график на высотных объектах Курской АЭС-2 и Михайловского ГОК."
      },
      career: {
        employers: ["АО «Трест Гидромонтаж»", "ООО «Проммонтаж-Курск»", "ПАО «МГОК им. Варичева»"],
        growth: "Монтажник 4 разряда → Бригадир монтажников металлоконструкций → Производитель работ (Прораб).",
        colleges: ["Курский монтажный техникум", "Курский политехнический колледж"]
      }
    },
    "truck-driver": {
      num: "10",
      title: "Водитель грузового автомобиля (БелАЗ 130т / категория C, CE)",
      category: "logistics",
      categoryName: "Транспорт и карьер",
      demand: 95,
      salary: "85 000 — 170 000 ₽",
      icon: "truck",
      shortDesc: "Управление карьерными автосамосвалами БелАЗ грузоподъемностью 130–220 тонн в чаше Михайловского железорудного карьера и магистральными тяжелыми автопоездами.",
      specs: {
        equipment: "Карьерные самосвалы БелАЗ-75131 с электромеханической трансмиссией, тягачи Scania/KAMAZ-54901, бортовые компьютеры карьерной навигации «Карьер».",
        materials: "Сырая железная руда, кварциты, скальная порода, крупногабаритное технологическое оборудование.",
        standards: "ПДД РФ, Федеральные нормы и правила в области промышленной безопасности на открытых горных работах."
      },
      qualification: {
        ranks: "Категории C, CE, права тракториста-машиниста категории А-III (карьерные самосвалы). Стаж от 3 лет.",
        tolerances: "Движение по серпантинам карьера глубиной свыше 380 метров при любых метеоусловиях, координация с экскаваторами ЭКГ-15.",
        shift: "Сменный график 2/2 по 12 часов с обязательным предрейсовым автоматизированным медосмотром."
      },
      career: {
        employers: ["ПАО «Михайловский ГОК им. А.В. Варичева» (Управление автотранспорта)", "ООО «Курскавтодор»", "АО «Курская птицефабрика» Логистик"],
        growth: "Водитель самосвала → Водитель-инструктор → Начальник автоколонны карьерного транспорта.",
        colleges: ["Железногорский политехнический колледж", "Курский автотехнический колледж"]
      }
    },
    "crane-operator": {
      num: "11",
      title: "Машинист крана (крановщик)",
      category: "heavy",
      categoryName: "Тяжелая промышленность",
      demand: 93,
      salary: "90 000 — 180 000 ₽",
      icon: "crane",
      shortDesc: "Управление башенными сверхтяжелыми кранами высокой грузоподъемности (Liebherr, Potain) и металлургическими литейными мостовыми кранами грузоподъемностью до 160 тонн.",
      specs: {
        equipment: "Тяжелые башенные краны Liebherr 1000 EC-H, мостовые двухбалочные краны металлургических цехов, микропроцессорные приборы безопасности ОНК-160.",
        materials: "Подъем и филигранный монтаж корпусов реакторов, парогенераторов, ковшей с жидким чугуном, тяжелых штампов.",
        standards: "ФНП «Правила безопасности опасных производственных объектов, на которых используются подъемные сооружения»."
      },
      qualification: {
        ranks: "5–6 разряд, допуск к работе на кранах грузоподъемностью свыше 50 тонн, отсутствие медицинских противопоказаний по высоте.",
        tolerances: "Точность опускания многотонного оборудования по меткам до 5 миллиметров без раскачивания груза.",
        shift: "Сменный график в обогреваемых комфортабельных кабинах с круговым обзором и климат-контролем."
      },
      career: {
        employers: ["АО «АСЭ» (Строительство Курской АЭС-2)", "ПАО «Михайловский ГОК»", "КЭАЗ", "АО «Электроагрегат»"],
        growth: "Машинист крана 4 разряда → Машинист тяжелого башенного крана 6 разряда → Механик кранового хозяйства предприятия.",
        colleges: ["Курский монтажный техникум", "ОБПОУ «КЭМТ»"]
      }
    }
  };

  // --- КУРСКИЕ ИНДУСТРИАЛЬНЫЕ ПРЕДПРИЯТИЯ (РЕЕСТР ТЕЛЕМЕТРИИ ДЛЯ HUD-LIBRARY) ---
  const ENTERPRISES_DATA = [
    { name: "Михайловский ГОК им. А.В. Варичева", sector: "Горнорудная", vacancies: 420, avgRate: "118 000 ₽", status: "Аккредитован", city: "Железногорск" },
    { name: "Курская АЭС-2 (ВВЭР-ТОИ)", sector: "Атомная энергетика", vacancies: 680, avgRate: "135 000 ₽", status: "Стратегический", city: "Курчатов" },
    { name: "Курский электроаппаратный завод (КЭАЗ)", sector: "Электротехника", vacancies: 195, avgRate: "94 000 ₽", status: "Федеральный лидер", city: "Курск" },
    { name: "АО «Электроагрегат»", sector: "Машиностроение", vacancies: 140, avgRate: "88 000 ₽", status: "ОПК / Аккредитован", city: "Курск" },
    { name: "АО «Авиаавтоматика им. В.В. Тарасова»", sector: "Приборостроение", vacancies: 115, avgRate: "92 000 ₽", status: "Высокотехнологичный", city: "Курск" },
    { name: "АО «Геомаш»", sector: "Буровое машиностроение", vacancies: 85, avgRate: "86 000 ₽", status: "Аккредитован", city: "Щигры / Курск" },
    { name: "АО «Совтест АТЕ»", sector: "Электронное приборостроение", vacancies: 65, avgRate: "105 000 ₽", status: "Инновационный центр", city: "Курск" },
    { name: "ООО «Курскхимволокно»", sector: "Химическая промышленность", vacancies: 130, avgRate: "82 000 ₽", status: "Действующий кластер", city: "Курск" },
    { name: "ОАО «Курскрезинотехника»", sector: "Промышленный синтез", vacancies: 160, avgRate: "78 000 ₽", status: "Аккредитован", city: "Курск" },
    { name: "Холдинг «ТИТАН-2» (Строительный дивизион)", sector: "Промышленное строительство", vacancies: 540, avgRate: "125 000 ₽", status: "Генеральный подрядчик", city: "Курчатов" }
  ];

  // --- BOOT 1: HARDWARE OPTICAL LOUPE SPLITTER ---
  function bootLoupe() {
    const loupe = $("#loupe");
    const stage = $("#loupe-stage");
    const splitter = $("#splitter");
    const glare = $("#loupe-glare");
    if (!loupe || !stage || !splitter) return;

    let dragging = false;

    function setSplit(pct) {
      pct = Math.max(8, Math.min(92, pct));
      loupe.style.setProperty("--split", pct + "%");
      const chip = $("#chip-split");
      if (chip) chip.textContent = `[ СРЕЗ: CAD ${Math.round(pct)}% // CNC ${100 - Math.round(pct)}% ]`;
    }

    function moveAt(clientX) {
      const rect = stage.getBoundingClientRect();
      if (!rect.width) return;
      const rel = clientX - rect.left;
      const pct = (rel / rect.width) * 100;
      setSplit(pct);
    }

    splitter.addEventListener("pointerdown", function (e) {
      e.preventDefault();
      e.stopPropagation();
      dragging = true;
      loupe.classList.add("is-dragging");
      splitter.setPointerCapture(e.pointerId);
    });

    window.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      moveAt(e.clientX);
    });

    window.addEventListener("pointerup", function () {
      if (dragging) {
        dragging = false;
        loupe.classList.remove("is-dragging");
      }
    });

    window.addEventListener("pointercancel", function () {
      if (dragging) {
        dragging = false;
        loupe.classList.remove("is-dragging");
      }
    });

    // 3D Parallax & Glare Tracking
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      let ticking = false;
      let targetRx = 0, targetRy = 0, currentRx = 0, currentRy = 0;

      function updateTilt() {
        currentRx += (targetRx - currentRx) * 0.1;
        currentRy += (targetRy - currentRy) * 0.1;
        loupe.style.transform = `rotateX(${currentRx.toFixed(2)}deg) rotateY(${currentRy.toFixed(2)}deg)`;
        if (Math.abs(targetRx - currentRx) > 0.04 || Math.abs(targetRy - currentRy) > 0.04) {
          window.requestAnimationFrame(updateTilt);
        } else {
          ticking = false;
        }
      }

      window.addEventListener("pointermove", function (e) {
        const w = window.innerWidth, h = window.innerHeight;
        const nx = (e.clientX / w) * 2 - 1;
        const ny = (e.clientY / h) * 2 - 1;
        targetRy = nx * 6;
        targetRx = -ny * 5;

        const gx = (e.clientX / w) * 100;
        const gy = (e.clientY / h) * 100;
        loupe.style.setProperty("--gx", `${gx.toFixed(1)}%`);
        loupe.style.setProperty("--gy", `${gy.toFixed(1)}%`);

        if (!ticking) {
          ticking = true;
          window.requestAnimationFrame(updateTilt);
        }
      }, { passive: true });
    }

    // Auto-demo oscillation at start
    setTimeout(() => {
      let startTime = performance.now();
      function bounce(now) {
        let elapsed = (now - startTime) / 1000;
        if (elapsed > 2.4 || dragging) return;
        let s = 46 + Math.sin(elapsed * 3.5) * 14;
        setSplit(s);
        requestAnimationFrame(bounce);
      }
      requestAnimationFrame(bounce);
    }, 800);
  }

  // --- BOOT 2: STICKY SIDEBAR SCROLL-SPY ---
  function bootSidebar() {
    const anchors = $$(".sidebar-anchor");
    if (!anchors.length) return;

    const sections = anchors.map(a => {
      const href = a.getAttribute("href");
      return href && href.startsWith("#") ? $(href) : null;
    }).filter(Boolean);

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = "#" + entry.target.id;
          anchors.forEach(a => {
            if (a.getAttribute("href") === id) {
              a.classList.add("is-active");
            } else {
              a.classList.remove("is-active");
            }
          });
        }
      });
    }, { rootMargin: "-30% 0px -40% 0px" });

    sections.forEach(sec => observer.observe(sec));
  }

  // --- BOOT 3: MOBILE BURGER MENU ---
  function bootMobileMenu() {
    const burger = $("#burger-btn");
    const nav = $("#site-nav");
    if (!burger || !nav) return;

    burger.addEventListener("click", () => {
      const open = document.body.classList.toggle("menu-open");
      burger.setAttribute("aria-expanded", String(open));
    });

    $$(".nav-pill", nav).forEach(link => {
      link.addEventListener("click", () => {
        document.body.classList.remove("menu-open");
        burger.setAttribute("aria-expanded", "false");
      });
    });
  }

  // --- BOOT 4: HUD MODALS & TABS ---
  function bootHUD() {
    const scrim = $("#hud-scrim");
    const libModal = $("#hud-library");
    const inspModal = $("#hud-inspector");
    const openLibBtn = $("#btn-open-library");
    const openLibHeroBtn = $("#btn-hero-library");

    function openModal(modal) {
      if (!modal) return;
      if (scrim) scrim.classList.add("is-open");
      modal.classList.add("is-open");
      document.body.style.overflow = "hidden";
    }

    function closeModal() {
      if (scrim) scrim.classList.remove("is-open");
      $$(".hud").forEach(m => m.classList.remove("is-open"));
      document.body.style.overflow = "";
    }

    if (openLibBtn) openLibBtn.addEventListener("click", () => openModal(libModal));
    if (openLibHeroBtn) openLibHeroBtn.addEventListener("click", () => openModal(libModal));
    if (scrim) scrim.addEventListener("click", closeModal);

    $$(".hud-close").forEach(btn => btn.addEventListener("click", closeModal));

    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeModal();
    });

    // Populate Enterprise Table in #hud-library
    const tbody = $("#library-tbody");
    if (tbody && !tbody.children.length) {
      tbody.innerHTML = ENTERPRISES_DATA.map(ent => `
        <tr>
          <td><strong style="color:#fff;">${ent.name}</strong><br><span style="font-size:11px; color:var(--text-dim);">${ent.city}</span></td>
          <td><span style="font-family:var(--mono); font-size:12px; color:var(--text-muted);">${ent.sector}</span></td>
          <td><span style="font-family:var(--mono); color:#ffffff; font-weight:600;">${ent.vacancies}</span></td>
          <td><span style="font-family:var(--mono); color:#e4e4e7;">${ent.avgRate}</span></td>
          <td>
            <span class="status-indicator">
              <span class="status-dot"></span> ${ent.status}
            </span>
          </td>
        </tr>
      `).join("");
    }

    // Modal Tabs logic (01, 02, 03)
    $$(".reader-tab").forEach(tab => {
      tab.addEventListener("click", function () {
        const paneId = this.getAttribute("data-pane");
        const container = this.closest(".hud") || document;
        $$(".reader-tab", container).forEach(t => t.classList.remove("is-active"));
        $$(".tab-pane", container).forEach(p => p.classList.remove("is-active"));
        this.classList.add("is-active");
        const targetPane = $(`#pane-${paneId}`, container);
        if (targetPane) targetPane.classList.add("is-active");
      });
    });

    // Expose openProfessionInspector globally
    window.openProfessionInspector = function (key) {
      const data = PROFESSIONS_DATA[key];
      if (!data) return;

      const titleEl = $("#inspector-title");
      const kickerEl = $("#inspector-kicker");
      const descEl = $("#inspector-desc");
      const specEl = $("#inspector-spec-content");
      const qualEl = $("#inspector-qual-content");
      const careerEl = $("#inspector-career-content");

      if (titleEl) titleEl.textContent = data.title;
      if (kickerEl) kickerEl.textContent = `ТЕЛЕМЕТРИЯ СПЕЦИАЛЬНОСТИ // РАЗРЯД ${data.num} // СПРОС ${data.demand}%`;
      if (descEl) descEl.textContent = data.shortDesc;

      if (specEl) {
        specEl.innerHTML = `
          <div style="display:flex; flex-direction:column; gap:16px;">
            <div style="padding:16px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.09); border-radius:12px;">
              <span style="font-family:var(--mono); font-size:10.5px; letter-spacing:0.06em; color:var(--text-dim); text-transform:uppercase;">Технологическое оборудование и стенды:</span>
              <p style="font-size:13.5px; color:#ffffff; line-height:1.55; margin-top:5px;">${data.specs.equipment}</p>
            </div>
            <div style="padding:16px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.09); border-radius:12px;">
              <span style="font-family:var(--mono); font-size:10.5px; letter-spacing:0.06em; color:var(--text-dim); text-transform:uppercase;">Обрабатываемые материалы и среды:</span>
              <p style="font-size:13.5px; color:#ffffff; line-height:1.55; margin-top:5px;">${data.specs.materials}</p>
            </div>
            <div style="padding:16px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.09); border-radius:12px;">
              <span style="font-family:var(--mono); font-size:10.5px; letter-spacing:0.06em; color:var(--text-dim); text-transform:uppercase;">Нормативные ГОСТ и правила Ростехнадзора:</span>
              <p style="font-size:13.5px; color:#ffffff; line-height:1.55; margin-top:5px;">${data.specs.standards}</p>
            </div>
          </div>
        `;
      }

      if (qualEl) {
        qualEl.innerHTML = `
          <div style="display:flex; flex-direction:column; gap:16px;">
            <div style="padding:16px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.09); border-radius:12px;">
              <span style="font-family:var(--mono); font-size:10.5px; letter-spacing:0.06em; color:var(--text-dim); text-transform:uppercase;">Квалификационные разряды и аттестация:</span>
              <p style="font-size:13.5px; color:#ffffff; line-height:1.55; margin-top:5px;">${data.qualification.ranks}</p>
            </div>
            <div style="padding:16px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.09); border-radius:12px;">
              <span style="font-family:var(--mono); font-size:10.5px; letter-spacing:0.06em; color:var(--text-dim); text-transform:uppercase;">Метрологические допуски и неразрушающий контроль:</span>
              <p style="font-size:13.5px; color:#ffffff; line-height:1.55; margin-top:5px;">${data.qualification.tolerances}</p>
            </div>
            <div style="padding:16px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.09); border-radius:12px;">
              <span style="font-family:var(--mono); font-size:10.5px; letter-spacing:0.06em; color:var(--text-dim); text-transform:uppercase;">Условия смены и средства индивидуальной защиты (СИЗ):</span>
              <p style="font-size:13.5px; color:#ffffff; line-height:1.55; margin-top:5px;">${data.qualification.shift}</p>
            </div>
          </div>
        `;
      }

      if (careerEl) {
        careerEl.innerHTML = `
          <div style="display:flex; flex-direction:column; gap:16px;">
            <div style="padding:16px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.09); border-radius:12px;">
              <span style="font-family:var(--mono); font-size:10.5px; letter-spacing:0.06em; color:var(--text-dim); text-transform:uppercase;">Ключевые работодатели Курской области:</span>
              <ul style="margin-top:6px; padding-left:20px; font-size:13px; color:#e4e4e7; line-height:1.5;">
                ${data.career.employers.map(e => `<li style="margin-bottom:4px;">${e}</li>`).join("")}
              </ul>
            </div>
            <div style="padding:16px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.09); border-radius:12px;">
              <span style="font-family:var(--mono); font-size:10.5px; letter-spacing:0.06em; color:var(--text-dim); text-transform:uppercase;">Вектор профессионального роста:</span>
              <p style="font-size:13.5px; color:#ffffff; line-height:1.55; margin-top:5px;">${data.career.growth}</p>
            </div>
            <div style="padding:16px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.09); border-radius:12px;">
              <span style="font-family:var(--mono); font-size:10.5px; letter-spacing:0.06em; color:var(--text-dim); text-transform:uppercase;">Базовые колледжи региона:</span>
              <p style="font-size:13.5px; color:#ffffff; line-height:1.55; margin-top:5px;">${data.career.colleges.join(" · ")}</p>
            </div>
          </div>
        `;
      }

      // Reset to first tab
      const firstTab = $(".reader-tab", inspModal);
      if (firstTab) firstTab.click();

      openModal(inspModal);
    };
  }

  // --- BOOT 5: VACANCIES FILTERING (ON VACANCIES.HTML) ---
  function bootVacanciesFilters() {
    const chips = $$(".filter-chip");
    const cards = $$(".bento-card");
    if (!chips.length || !cards.length) return;

    chips.forEach(chip => {
      chip.addEventListener("click", function () {
        chips.forEach(c => c.classList.remove("is-active"));
        this.classList.add("is-active");

        const filter = this.getAttribute("data-filter");
        cards.forEach(card => {
          const category = card.getAttribute("data-category");
          if (filter === "all" || category === filter) {
            card.style.display = "flex";
            card.style.animation = "fadeScale 0.4s var(--ease) both";
          } else {
            card.style.display = "none";
          }
        });
      });
    });

    // Attach card inspection clicks
    cards.forEach(card => {
      card.addEventListener("click", () => {
        const key = card.getAttribute("data-key");
        if (key && window.openProfessionInspector) {
          window.openProfessionInspector(key);
        }
      });
    });

    // Check URL search params (e.g. ?sector=power)
    const urlSector = new URLSearchParams(window.location.search).get("sector");
    if (urlSector) {
      const targetChip = chips.find(c => c.getAttribute("data-filter") === urlSector);
      if (targetChip) targetChip.click();
    }
  }

  // --- BOOT 6: INTERACTIVE CAREER QUIZ (ON EDUCATION.HTML) ---
  function bootCareerQuiz() {
    const quizRoot = $("#career-quiz");
    if (!quizRoot) return;

    const QUIZ_QUESTIONS = [
      {
        q: "1. Какая сфера технической деятельности вас больше всего привлекает?",
        options: [
          { text: "Высокоточное программирование и обработка металла на станках ЧПУ", score: "cnc-operator" },
          { text: "Высоковольтные подстанции, распределительные щиты и электротехника", score: "electrician-repair" },
          { text: "Монтаж металлоконструкций и аргонодуговая сварка реакторных узлов", score: "welding" },
          { text: "Управление сверхтяжелой техникой: карьерными БелАЗами и мощными кранами", score: "truck-driver" }
        ]
      },
      {
        q: "2. С какими типами чертежей и задач вам комфортнее работать?",
        options: [
          { text: "3D CAD-модели деталей, допуски до микрометров и шероховатость Ra", score: "cnc-operator" },
          { text: "Однолинейные электрические схемы, фазировка, релейная защита", score: "electrician-repair" },
          { text: "Карты сварных швов под ультразвуковой контроль (УЗК) и радиографию", score: "welding" },
          { text: "Карты карьерных маршрутов и схемы строповки многотонных грузов", score: "crane-operator" }
        ]
      },
      {
        q: "3. Какое ведущее предприятие Курской области вас вдохновляет масштабом?",
        options: [
          { text: "Курская АЭС-2 — строительство энергоблоков поколения III+ ВВЭР-ТОИ", score: "welding" },
          { text: "Михайловский ГОК им. Варичева — гигантский карьер и обогатительные фабрики", score: "truck-driver" },
          { text: "КЭАЗ — инновационное производство низко- и высоковольтной аппаратуры", score: "electrician-repair" },
          { text: "ОБПОУ «КЭМТ» — прецизионная лаборатория мехатроники и 5-осевого ЧПУ", score: "cnc-operator" }
        ]
      },
      {
        q: "4. Какой рабочий инструмент вызывает наибольшее уважение?",
        options: [
          { text: "Высокоточный микрометр, индикатор часового типа и пульт Fanuc", score: "cnc-operator" },
          { text: "TIG-горелка с аргоновым соплом и сварочная маска с автозатемнением", score: "welding" },
          { text: "Цифровой мультиметр, мегомметр и тепловизор Fluke", score: "electrician-repair" },
          { text: "Джойстики управления башенным краном и кабина карьерного самосвала", score: "crane-operator" }
        ]
      },
      {
        q: "5. Какой карьерный ориентир для вас приоритетен в ближайшие 3–5 лет?",
        options: [
          { text: "Стать наладчиком ЧПУ высшего разряда с доходом от 150 000 ₽", score: "cnc-operator" },
          { text: "Получить допуск НАКС и строить атомные энергоблоки по всей стране", score: "welding" },
          { text: "Стать главным энергетиком крупного промышленного комплекса", score: "electrician-repair" },
          { text: "Мастерски управлять тяжелой строительной техникой высокой грузоподъемности", score: "crane-operator" }
        ]
      }
    ];

    let currentStep = 0;
    const scores = {};

    function renderQuestion() {
      const q = QUIZ_QUESTIONS[currentStep];
      const fill = $("#quiz-progress-fill");
      const stepInd = $("#quiz-step-indicator");
      const titleEl = $("#quiz-question-title");
      const optionsWrap = $("#quiz-options-list");

      if (fill) fill.style.width = `${((currentStep + 1) / QUIZ_QUESTIONS.length) * 100}%`;
      if (stepInd) stepInd.textContent = `ВОПРОС 0${currentStep + 1} ИЗ 0${QUIZ_QUESTIONS.length}`;
      if (titleEl) titleEl.textContent = q.q;

      if (optionsWrap) {
        optionsWrap.innerHTML = q.options.map((opt, idx) => `
          <button class="quiz-option-btn" type="button" data-score="${opt.score}">
            <span>${opt.text}</span>
            <span style="font-family:var(--mono); font-size:12px; color:rgba(255,255,255,0.4);">→</span>
          </button>
        `).join("");

        $$(".quiz-option-btn", optionsWrap).forEach(btn => {
          btn.addEventListener("click", function () {
            const sc = this.getAttribute("data-score");
            scores[sc] = (scores[sc] || 0) + 1;
            currentStep++;
            if (currentStep < QUIZ_QUESTIONS.length) {
              renderQuestion();
            } else {
              renderResult();
            }
          });
        });
      }
    }

    function renderResult() {
      let topProfKey = "cnc-operator";
      let maxScore = -1;
      for (const [k, v] of Object.entries(scores)) {
        if (v > maxScore) {
          maxScore = v;
          topProfKey = k;
        }
      }

      const prof = PROFESSIONS_DATA[topProfKey] || PROFESSIONS_DATA["cnc-operator"];
      const wrap = $("#quiz-content");
      if (!wrap) return;

      wrap.innerHTML = `
        <div class="quiz-result-card" style="animation: fadeScale 0.5s var(--ease) both;">
          <div class="quiz-result-kicker">✓ РЕЗУЛЬТАТ АНАЛИЗА ПРОФИЛЯ СОВМЕСТИМОСТИ</div>
          <h3 class="quiz-result-prof">${prof.title}</h3>
          <p class="quiz-result-info">${prof.shortDesc}</p>

          <div class="quiz-result-meta">
            <div class="quiz-result-meta-item">
              <span class="quiz-result-meta-lbl">Спрос в регионе</span>
              <span class="quiz-result-meta-val" style="color:#ffffff;">${prof.demand}% (Критический)</span>
            </div>
            <div class="quiz-result-meta-item">
              <span class="quiz-result-meta-lbl">Стартовая вилка</span>
              <span class="quiz-result-meta-val" style="color:#e4e4e7;">${prof.salary}</span>
            </div>
            <div class="quiz-result-meta-item">
              <span class="quiz-result-meta-lbl">Базовый колледж</span>
              <span class="quiz-result-meta-val">${prof.career.colleges[0]}</span>
            </div>
          </div>

          <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
            <button class="btn btn-solid" id="btn-quiz-inspect" type="button">Изучить техкарту профессии</button>
            <button class="btn btn-ghost" id="btn-quiz-reset" type="button">Пройти тест заново</button>
          </div>
        </div>
      `;

      const inspectBtn = $("#btn-quiz-inspect");
      if (inspectBtn) {
        inspectBtn.addEventListener("click", () => {
          if (window.openProfessionInspector) window.openProfessionInspector(topProfKey);
        });
      }

      const resetBtn = $("#btn-quiz-reset");
      if (resetBtn) {
        resetBtn.addEventListener("click", () => {
          currentStep = 0;
          for (let k in scores) delete scores[k];
          location.reload();
        });
      }
    }

    renderQuestion();
  }

  // --- BOOT 7: VIDEO CONTROLS ---
  function bootVideoControls() {
    const video = $("#showcase-video");
    const playBtn = $("#video-btn-play");
    const muteBtn = $("#video-btn-mute");
    if (!video || !playBtn) return;

    playBtn.addEventListener("click", () => {
      if (video.paused) {
        video.play();
        playBtn.innerHTML = `<svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>`;
      } else {
        video.pause();
        playBtn.innerHTML = `<svg viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>`;
      }
    });

    if (muteBtn) {
      muteBtn.addEventListener("click", () => {
        video.muted = !video.muted;
        muteBtn.style.opacity = video.muted ? "0.6" : "1";
      });
    }
  }

  // --- INITIALIZE ALL MODULES ON DOM READY ---
  document.addEventListener("DOMContentLoaded", function () {
    bootLoupe();
    bootSidebar();
    bootMobileMenu();
    bootHUD();
    bootVacanciesFilters();
    bootCareerQuiz();
    bootVideoControls();
  });
})();
