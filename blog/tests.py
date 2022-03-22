from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post



class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='Do It Django')
        #print(logo_btn.attrs.values())
        self.assertEqual(logo_btn.attrs['href'], '/')

        #print(navbar.text)
        home_btn = navbar.find('a', text='Home')
        #print(home_btn)
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')




    def test_post_list(self):
        # 1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        #print(response.content)

        # 1.2 정상적으로 페이지가 로드 된다.
        self.assertEqual(response.status_code, 200)

        # 1.3 페이지 타이틀은 'Blog'이다.
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(soup.title.text)
        self.assertEqual(soup.title.text, 'Blog ')


        self.navbar_test(soup)

        # 2.1 메인 영역에 게시물이 하나도 없다면
        #print(Post.objects.count())
        self.assertEqual(Post.objects.count(), 0)
        # 2.2 '아직 게시물이 없습니다.'라는 문구가 보인다.
        main_area = soup.find('div', id='main-area')
        #print(f'test_main-area: {main_area}')
        self.assertIn('아직 게시물이 없습니다', main_area.text)
        #content = soup.find('p', id='con')
        #print(content.text)

        # 3.1 게시물이 2개 있다면

        post_001 = Post.objects.create(
            title='첫번째 포스트',
            content='Hello World. We are the world.',
            author=self.user_trump
        )
        post_002 = Post.objects.create(
            title='두 번째 포스트',
            content='1등이 전부는 아니잖아요?',
            author=self.user_obama
        )
        self.assertEqual(Post.objects.count(), 2)
        # 3.2 포스트 목록 페이지를 새로고침했을때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        #print(main_area)
        #aaa = main_area.find('p', id='con')
        #print(aaa.text)
        # 3.4 '아직 게시물이 없습니다'라는 문구는 더 이상 보이지 않는다.
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

    def test_post_detail(self):

        # 1.1 포스트가 하나 있다.
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello world. We are the world.',
            author=self.user_trump
        )


        # 1.2 그 포스트이 url '/blog/1' 이다.
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')
        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1 첫 번째 포스트의 url로 접근하면 정상적으로 작동한다.
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2 포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        self.navbar_test(soup)

        # 2.3 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(post_001.title, soup.title.text)
        # 2.4 첫 번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)
        #print(post_area.text)
        # 2.5 첫 번째 포스트이 작성자(author)가 포스트 영역에 있다.
        self.assertIn(self.user_trump.username.upper(), post_area.text)


        # 2.6 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(post_001.content, post_area.text)

        com_area = soup.find('div', id='comments-area')
        #print(com_area.text)
        self.assertIn("Submit", com_area.text)





