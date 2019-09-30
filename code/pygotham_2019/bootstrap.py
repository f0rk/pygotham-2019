from pygotham_2019 import meta, model


if __name__ == "__main__":
    meta.Base.metadata.drop_all(bind=meta.session.bind)
    meta.Base.metadata.create_all(bind=meta.session.bind)
    meta.session.commit()
