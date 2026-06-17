from django.core.management.base import BaseCommand
from apps.curriculum.models import Track, Subject
from apps.lessons.models import Lesson, ContentBlock


SEED_DATA = [
    {
        'track': {
            'title': 'Quran Sciences',
            'slug': 'quran-sciences',
            'description': 'A structured journey through the sciences of the Quran — from recitation to deep tafsir.',
            'order': 1,
            'is_published': True,
        },
        'subjects': [
            {
                'title': 'Introduction to Tafsir',
                'slug': 'intro-to-tafsir',
                'description': 'Foundations of Quranic interpretation — methodology, scholars, and key terms.',
                'order': 1,
                'is_published': True,
                'lessons': [
                    {
                        'title': 'What is Tafsir?',
                        'slug': 'what-is-tafsir',
                        'summary': 'An introduction to the discipline of Quranic exegesis — its meaning, origin, and why it matters.',
                        'order': 1,
                        'status': 'published',
                        'estimated_minutes': 10,
                        'content_blocks': [
                            {
                                'type': 'text',
                                'order': 1,
                                'body': {
                                    'text': 'Tafsir (تفسير) literally means "explanation" or "interpretation." As a discipline, it refers to the scholarly effort to uncover and explain the meanings of the Quran — linguistically, contextually, and spiritually.'
                                },
                            },
                            {
                                'type': 'verse',
                                'order': 2,
                                'body': {
                                    'surah': 75,
                                    'ayah': 19,
                                    'arabic': 'ثُمَّ إِنَّ عَلَيْنَا بَيَانَهُ',
                                    'translation': 'Then upon Us is its clarification.',
                                },
                            },
                            {
                                'type': 'text',
                                'order': 3,
                                'body': {
                                    'text': 'Allah ﷻ Himself promises clarification of the Quran. This is fulfilled through the Prophet ﷺ, who was the first and greatest mufassir. His explanations, recorded in the Sunnah, form the bedrock of all subsequent tafsir literature.'
                                },
                            },
                            {
                                'type': 'hadith',
                                'order': 4,
                                'body': {
                                    'text': 'The best of you are those who learn the Quran and teach it.',
                                    'source': 'Sahih al-Bukhari 5027',
                                    'narrator': 'Uthman ibn Affan (رضي الله عنه)',
                                },
                            },
                            {
                                'type': 'text',
                                'order': 5,
                                'body': {
                                    'text': 'A mufassir (exegete) must master multiple disciplines: Arabic linguistics and grammar, the circumstances of revelation (Asbab al-Nuzul), abrogation (Nasikh wa Mansukh), and the overall objectives of the Quran (Maqasid).'
                                },
                            },
                            {
                                'type': 'text',
                                'order': 6,
                                'body': {
                                    'text': 'The companion Ibn Abbas (رضي الله عنه) is widely regarded as the "Translator of the Quran" (Tarjuman al-Quran). The Prophet ﷺ made dua for him: "O Allah, give him deep understanding of the religion and teach him interpretation."'
                                },
                            },
                            {
                                'type': 'text',
                                'order': 7,
                                'body': {
                                    'text': 'Now test your understanding of what you have just read with the question below.'
                                },
                            },
                            {
                                'type': 'quiz',
                                'order': 8,
                                'body': {
                                    'question': 'Who is considered the "Translator of the Quran" (Tarjuman al-Quran) among the Companions?',
                                    'options': [
                                        'Abu Bakr al-Siddiq (رضي الله عنه)',
                                        'Umar ibn al-Khattab (رضي الله عنه)',
                                        'Ibn Abbas (رضي الله عنه)',
                                        'Ali ibn Abi Talib (رضي الله عنه)',
                                    ],
                                    'correct': 2,
                                    'explanation': 'Abdullah ibn Abbas (رضي الله عنه) earned this title due to his extraordinary mastery of Quranic interpretation, supported by the Prophet\'s ﷺ special dua for him.',
                                },
                            },
                        ],
                    },
                    {
                        'title': 'Schools of Tafsir',
                        'slug': 'schools-of-tafsir',
                        'summary': 'The major methodological schools in Quranic commentary and what distinguishes them.',
                        'order': 2,
                        'status': 'published',
                        'estimated_minutes': 12,
                        'content_blocks': [
                            {
                                'type': 'text',
                                'order': 1,
                                'body': {
                                    'text': 'Scholars have identified several broad schools (manhaj) of tafsir, each emphasising different tools and methods. Understanding these schools helps the student read classical commentaries critically and contextually.'
                                },
                            },
                            {
                                'type': 'text',
                                'order': 2,
                                'body': {
                                    'text': 'Tafsir bil-Mathur (روايي) — Interpretation by narration. This is the highest-ranked method: explaining the Quran with the Quran itself, then the Sunnah, then the statements of the Companions, then the Successors (Tabi\'un). Major works: Tafsir al-Tabari, Tafsir Ibn Kathir.'
                                },
                            },
                            {
                                'type': 'text',
                                'order': 3,
                                'body': {
                                    'text': 'Tafsir bil-Ra\'y (دراية) — Interpretation by considered opinion. This school applies Arabic linguistics, legal principles, and rational analysis. It is considered valid when grounded in established tools and not contradicting transmitted narrations.'
                                },
                            },
                            {
                                'type': 'hadith',
                                'order': 4,
                                'body': {
                                    'text': 'Whoever interprets the Quran based on his own opinion, let him take his seat in the Fire.',
                                    'source': 'Jami al-Tirmidhi 2951',
                                    'narrator': 'Ibn Abbas (رضي الله عنه)',
                                },
                            },
                            {
                                'type': 'text',
                                'order': 5,
                                'body': {
                                    'text': 'This hadith warns against tafsir driven purely by whim or ideology — not against scholarly reasoning (ijtihad) that is disciplined, evidence-based, and submissive to the text.'
                                },
                            },
                            {
                                'type': 'quiz',
                                'order': 6,
                                'body': {
                                    'question': 'Which of the following is an example of Tafsir bil-Mathur?',
                                    'options': [
                                        'Interpreting a verse using modern scientific discoveries',
                                        'Explaining a verse using another verse of the Quran',
                                        'Using philosophical reasoning to derive meaning',
                                        'Relying solely on personal linguistic analysis',
                                    ],
                                    'correct': 1,
                                    'explanation': 'Tafsir bil-Mathur (by narration) means explaining the Quran with the Quran itself, then the Sunnah, then the Companions\' statements. Explaining one verse using another verse is the purest form of this method.',
                                },
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        'track': {
            'title': 'Islamic Jurisprudence',
            'slug': 'fiqh',
            'description': 'From Usul al-Fiqh to practical rulings — a grounded study of Islamic law.',
            'order': 2,
            'is_published': True,
        },
        'subjects': [
            {
                'title': 'Principles of Fiqh (Usul)',
                'slug': 'usul-al-fiqh',
                'description': 'The theoretical foundations that underpin Islamic legal reasoning.',
                'order': 1,
                'is_published': True,
                'lessons': [
                    {
                        'title': 'Sources of Islamic Law',
                        'slug': 'sources-of-islamic-law',
                        'summary': 'Quran, Sunnah, Ijma, and Qiyas — the four primary sources of Islamic jurisprudence.',
                        'order': 1,
                        'status': 'published',
                        'estimated_minutes': 12,
                        'content_blocks': [
                            {
                                'type': 'text',
                                'order': 1,
                                'body': {
                                    'text': 'Islamic law (Sharia) is not arbitrary — it is derived from specific, hierarchically ordered sources. The majority of classical scholars agree on four primary sources.'
                                },
                            },
                            {
                                'type': 'verse',
                                'order': 2,
                                'body': {
                                    'surah': 4,
                                    'ayah': 59,
                                    'arabic': 'يَا أَيُّهَا الَّذِينَ آمَنُوا أَطِيعُوا اللَّهَ وَأَطِيعُوا الرَّسُولَ وَأُولِي الْأَمْرِ مِنكُمْ',
                                    'translation': 'O you who believe! Obey Allah, and obey the Messenger, and those in authority among you.',
                                },
                            },
                            {
                                'type': 'text',
                                'order': 3,
                                'body': {
                                    'text': 'Scholars derive from this verse the first two sources: the Quran (obey Allah) and the Sunnah (obey the Messenger). The verse continues: "If you disagree about something, refer it to Allah and the Messenger" — pointing to the role of scholarly consensus and analogy when direct texts are absent.'
                                },
                            },
                            {
                                'type': 'text',
                                'order': 4,
                                'body': {
                                    'text': 'The four sources are: (1) Quran — the direct word of Allah; (2) Sunnah — the Prophet\'s ﷺ statements, actions, and tacit approvals; (3) Ijma — unanimous consensus of qualified scholars; (4) Qiyas — analogical reasoning from established rulings.'
                                },
                            },
                            {
                                'type': 'quiz',
                                'order': 5,
                                'body': {
                                    'question': 'What is the correct order of the four primary sources of Islamic law?',
                                    'options': [
                                        'Sunnah → Quran → Qiyas → Ijma',
                                        'Quran → Sunnah → Ijma → Qiyas',
                                        'Ijma → Quran → Sunnah → Qiyas',
                                        'Quran → Ijma → Sunnah → Qiyas',
                                    ],
                                    'correct': 1,
                                    'explanation': 'The Quran is the primary source, followed by the Sunnah which explains and details it. Ijma (scholarly consensus) comes third, and Qiyas (analogy) fourth. This hierarchy is agreed upon by the majority of classical jurists.',
                                },
                            },
                        ],
                    },
                    {
                        'title': 'What is Ijtihad?',
                        'slug': 'what-is-ijtihad',
                        'summary': 'Independent legal reasoning — who can do it, when, and what are its limits.',
                        'order': 2,
                        'status': 'published',
                        'estimated_minutes': 10,
                        'content_blocks': [
                            {
                                'type': 'text',
                                'order': 1,
                                'body': {
                                    'text': 'Ijtihad (اجتهاد) means "striving" or "exerting effort." In Islamic law, it refers to the process by which a qualified scholar derives rulings on new or ambiguous matters by applying established legal principles to available evidence.'
                                },
                            },
                            {
                                'type': 'hadith',
                                'order': 2,
                                'body': {
                                    'text': 'When a judge strives to reach a verdict and gets it right, he gets two rewards. If he strives and makes an error, he gets one reward.',
                                    'source': 'Sahih al-Bukhari 7352, Sahih Muslim 1716',
                                    'narrator': 'Amr ibn al-As (رضي الله عنه)',
                                },
                            },
                            {
                                'type': 'text',
                                'order': 3,
                                'body': {
                                    'text': 'Not everyone is qualified to perform ijtihad. Classical scholars set rigorous conditions: mastery of Arabic, deep knowledge of the Quran and Sunnah, familiarity with consensus positions, understanding of legal objectives (Maqasid), and expertise in analogical reasoning.'
                                },
                            },
                            {
                                'type': 'quiz',
                                'order': 4,
                                'body': {
                                    'question': 'What does the hadith about the judge\'s reward tell us about ijtihad?',
                                    'options': [
                                        'Only correct ijtihad is rewarded; errors are sinful',
                                        'Scholars should avoid ijtihad to prevent errors',
                                        'A sincere, qualified scholar is rewarded even when mistaken',
                                        'Ijtihad is only valid for judges, not scholars',
                                    ],
                                    'correct': 2,
                                    'explanation': 'The hadith shows that Allah ﷻ rewards sincere scholarly effort (ijtihad) regardless of outcome — two rewards for a correct ruling, one for an earnest but mistaken one. This encourages scholars to engage with new questions rather than avoid them.',
                                },
                            },
                        ],
                    },
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample curriculum, subject, and lesson data'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing data before seeding')

    def handle(self, *args, **options):
        if options['clear']:
            Lesson.objects.all().delete()
            Subject.objects.all().delete()
            Track.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared existing curriculum data.'))

        for entry in SEED_DATA:
            track_data = entry['track']
            track, created = self._get_or_create_track(track_data)
            action = 'Created' if created else 'Skipped (exists)'
            self.stdout.write(f'  Track [{action}]: {track.title}')

            for subject_data in entry['subjects']:
                lessons_data = subject_data.pop('lessons', [])
                subject, created = self._get_or_create_subject(subject_data, track)
                action = 'Created' if created else 'Skipped (exists)'
                self.stdout.write(f'    Subject [{action}]: {subject.title}')

                for lesson_data in lessons_data:
                    blocks_data = lesson_data.pop('content_blocks', [])
                    lesson, created = self._get_or_create_lesson(lesson_data, subject, blocks_data)
                    action = 'Created' if created else 'Skipped (exists)'
                    self.stdout.write(f'      Lesson [{action}]: {lesson.title}')

        self.stdout.write(self.style.SUCCESS('Seed complete.'))

    def _get_or_create_track(self, data):
        existing = Track.objects(slug=data['slug']).first()
        if existing:
            return existing, False
        track = Track(**data)
        track.save()
        return track, True

    def _get_or_create_subject(self, data, track):
        existing = Subject.objects(slug=data['slug']).first()
        if existing:
            return existing, False
        subject = Subject(track=track, **data)
        subject.save()
        return subject, True

    def _get_or_create_lesson(self, data, subject, blocks_data):
        existing = Lesson.objects(slug=data['slug']).first()
        if existing:
            return existing, False
        blocks = [ContentBlock(**b) for b in blocks_data]
        lesson = Lesson(subject=subject, content_blocks=blocks, **data)
        lesson.save()
        return lesson, True
