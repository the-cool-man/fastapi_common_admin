from fastapi.responses import JSONResponse
from ..models import SiteConfig, SocialMedia as Social, PublicPageSEO as PageSEO, CmsPageModel as CmsPage, EmailTemplateModel as EmailTemplate, SMSTemplateModel as SmsTemplates

import os
import time
from pathlib import Path
import uuid

UPLOAD_DIR = "uploads"
LOGO_DIR = os.path.join(UPLOAD_DIR, "logos")
FAVICON_DIR = os.path.join(UPLOAD_DIR, "favicons")
SOCIAL_LOGO_DIR = os.path.join(UPLOAD_DIR, "social")
PAGE_SEO_DIR = os.path.join(UPLOAD_DIR, "seoImage")


async def handleDashboardData(db):
    try:
        dashboard_data = {
            "cms_pages_count": db.query(CmsPage).count(),
            "social_networking_links_count": db.query(Social).count(),
            "public_pages_seo_count": db.query(PageSEO).count(),
            "email_templates_count": db.query(EmailTemplate).count(),
            "sms_templates_count": db.query(SmsTemplates).count(),
        }

        return {
            "status": "success",
            "message": "All Dashboard Data",
            "data": dashboard_data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": {}
        }


async def handleLogoFavicon(request_data, db):
    logo_filename = None
    favicon_filename = None
    logo_path = None
    favicon_path = None
    try:
        site_config = None
        if getattr(request_data, "id", None):
            site_config = db.query(SiteConfig).filter(
                SiteConfig.id == request_data.id).first()
            print("request_data", request_data)
            # if not site_config:
            #     return {"status": "error", "message": "Record Not Found"}
            # message = "updated"
        if not site_config:
            site_config = SiteConfig()
            db.add(site_config)
            message = "inserted"
        else:
            message = "updated"

        if request_data.logo:
            if site_config.logo:
                old_logo_path = os.path.join(LOGO_DIR, site_config.logo)
                if os.path.exists(old_logo_path):
                    os.remove(old_logo_path)

            fileName = request_data.logo.filename
            ext = os.path.splitext(fileName)[1]
            unique_str = f"{int(time.time())}{uuid.uuid4().hex[:10]}"
            logo_filename = f"{unique_str}{ext}"
            logo_path = os.path.join(LOGO_DIR, logo_filename)

            with open(logo_path, "wb") as bufferFile:
                bufferFile.write(await request_data.logo.read())

            site_config.logo = logo_filename

        if request_data.favicon:
            if site_config.favicon:
                old_favicon_path = os.path.join(
                    FAVICON_DIR, site_config.favicon)
                if os.path.exists(old_favicon_path):
                    os.remove(old_favicon_path)

            fileName = request_data.favicon.filename
            ext = os.path.splitext(fileName)[1]
            unique_str = f"{int(time.time())}{uuid.uuid4().hex[:10]}"
            favicon_filename = f"{unique_str}{ext}"
            favicon_path = os.path.join(FAVICON_DIR, favicon_filename)
            with open(favicon_path, "wb") as bufferFile:
                bufferFile.write(await request_data.favicon.read())

            site_config.favicon = favicon_filename

        db.commit()
        db.refresh(site_config)

        return {"status": "success", "message": f"Data {message} successfully"}

    except Exception as e:
        db.rollback()
        # Cleanup newly uploaded files if DB operation fails
        if logo_path and os.path.exists(logo_path):
            os.remove(logo_path)
        if favicon_path and os.path.exists(favicon_path):
            os.remove(favicon_path)
        return {"status": "error", "message": f"DB Error: {str(e)}"}


async def handleCommonSetting(request_data, db):
    try:
        if getattr(request_data, "id", None):
            site_config = db.query(SiteConfig).filter(
                SiteConfig.id == request_data.id).first()
            if not site_config:
                return {"status": "error", "message": "Record Not Found"}
            message = "updated"
        else:
            site_config = SiteConfig()
            db.add(site_config)   # add new object to session
            message = "inserted"

        for field in [
            "contact_no", "google_analytics_code", "footer_text", "about_footer",
            "full_address", "web_name", "web_frienly_name", "website_title",
            "website_description", "website_keywords", "map_address", "timezone"
        ]:
            value = getattr(request_data, field, None)
            if value is not None:
                setattr(site_config, field, value)

        db.commit()
        db.refresh(site_config)

        return {"status": "success", "message": f"Data {message} successfully"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": f"DB Error: {str(e)}"}


async def handleEmailSetting(request_data, db):
    try:
        if getattr(request_data, 'id', None):
            site_config = db.query(SiteConfig).filter(
                SiteConfig.id == request_data.id).first()
            if site_config is None:
                return {"status": "error", "message": "Record Not Found"}
            message = "Updated"

        else:
            site_config = SiteConfig()
            db.add(site_config)
            message = "Inserted"

        site_config.from_email = request_data.from_email
        site_config.contact_email = request_data.contact_email

        db.commit()
        # db.refresh(site_config)
        return {"status": "success", "message": f"Data {message} Successfully"}

    except Exception as err:
        return {"status": "error", "message": str(err)}


async def handleSocialMedia(request_data, db):

    try:
        if request_data.id is None:
            is_name_exist = db.query(Social).filter(
                Social.social_name == request_data.social_name
            ).first()
            if is_name_exist:
                return JSONResponse(
                    content={"status": "error",
                             "message": "social_name has already been taken."},
                    status_code=200
                )
            social_data = Social()
            message = "inserted"
        else:
            social_data = db.query(Social).filter(
                Social.id == request_data.id
            ).first()

            if not social_data:
                return JSONResponse(
                    content={"status": "error",
                             "message": "Record not found!"},
                    status_code=200
                )
            if db.query(Social).filter(
                Social.social_name == request_data.social_name, Social.id != request_data.id
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "social_name has already been taken."},
                    status_code=200
                )

            message = "updated"

        if request_data.social_logo:
            if social_data.social_logo:
                old_path = os.path.join(
                    SOCIAL_LOGO_DIR, social_data.social_logo)
                if os.path.exists(old_path):
                    os.remove(old_path)

            file_name = request_data.social_logo.filename
            ext = os.path.splitext(file_name)[1]
            unique_str = f"{int(time.time())}{uuid.uuid4().hex[:10]}"
            logo_filename = f"{unique_str}{ext}"
            logo_path = os.path.join(SOCIAL_LOGO_DIR, logo_filename)

            with open(logo_path, "wb") as file:
                file.write(await request_data.social_logo.read())

            social_data.social_logo = logo_filename

        social_data.social_name = request_data.social_name
        social_data.social_link = request_data.social_link
        social_data.status = request_data.status

        db.add(social_data)
        db.commit()
        db.refresh(social_data)

        return JSONResponse(
            content={
                "status": "success",
                "message": f"Social media link {message} successfully",
            },
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=200
        )


async def handlePublicPageSEO(request_data, db):

    try:
        if request_data.id is None:
            is_name_exist = db.query(PageSEO).filter(
                PageSEO.page_name == request_data.page_name
            ).first()
            if is_name_exist:
                return JSONResponse(
                    content={"status": "error",
                             "message": "page_name has already been taken."},
                    status_code=200
                )
            social_data = PageSEO()
            message = "inserted"
        else:
            social_data = db.query(PageSEO).filter(
                PageSEO.id == request_data.id
            ).first()

            if not social_data:
                return JSONResponse(
                    content={"status": "error",
                             "message": "Record not found!"},
                    status_code=200
                )
            if db.query(PageSEO).filter(
                PageSEO.page_name == request_data.page_name, PageSEO.id != request_data.id
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "page_name has already been taken."},
                    status_code=200
                )

            message = "updated"

        if request_data.meta_image:
            if social_data.meta_image:
                old_path = os.path.join(
                    PAGE_SEO_DIR, social_data.meta_image)
                if os.path.exists(old_path):
                    os.remove(old_path)

            file_name = request_data.meta_image.filename
            ext = os.path.splitext(file_name)[1]
            unique_str = f"{int(time.time())}{uuid.uuid4().hex[:10]}"
            logo_filename = f"{unique_str}{ext}"
            logo_path = os.path.join(PAGE_SEO_DIR, logo_filename)

            with open(logo_path, "wb") as file:
                file.write(await request_data.meta_image.read())

            social_data.meta_image = logo_filename

        social_data.page_name = request_data.page_name
        social_data.meta_title = request_data.meta_title
        social_data.meta_description = request_data.meta_description
        social_data.status = request_data.status

        db.add(social_data)
        db.commit()
        db.refresh(social_data)

        return JSONResponse(
            content={
                "status": "success",
                "message": f"Public Page SEO {message} successfully",
            },
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=200
        )
