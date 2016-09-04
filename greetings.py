#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import model
from sqlalchemy.orm import sessionmaker

from utils import store_segment, store_doc

Session = sessionmaker(bind=model.engine)

session = Session()

doc = store_doc(session, 'cc_k1', 'Kitchen Command & Control #1')

# remove DocumentSegmentMap entries for this document

session.query(model.DocumentSegmentMap).filter(model.DocumentSegmentMap.doc==doc).delete()

store_segment (session, doc, 'Guten Morgen, HAL!',  set(['greeting(s)', 'formal(s)', 'personal(s)']))
store_segment (session, doc, 'Guten Morgen!',       set(['greeting(s)', 'formal(s)']))
store_segment (session, doc, 'Hallo HAL!',          set(['greeting(s)', 'informal(s)', 'personal(s)']))
store_segment (session, doc, 'Hallo',               set(['greeting(s)', 'informal(s)']))
store_segment (session, doc, 'Hi',                  set(['greeting(s)', 'informal(s)']))
store_segment (session, doc, 'Hi Computer',         set(['greeting(s)', 'informal(s)', 'personal(s)']))
store_segment (session, doc, 'Hallo Computer!',     set(['greeting(s)', 'informal(s)', 'personal(s)']))
store_segment (session, doc, 'Guten Tag Computer!', set(['greeting(s)', 'formal(s)', 'personal(s)']))
store_segment (session, doc, 'Tag Computer!',       set(['greeting(s)', 'informal(s)', 'personal(s)']))
store_segment (session, doc, 'Morgen Computer!',    set(['greeting(s)', 'informal(s)', 'personal(s)']))
store_segment (session, doc, 'Huch!',               set(['oops(s)']))
store_segment (session, doc, 'Hoppla!',             set(['oops(s)']))
store_segment (session, doc, 'Troet!',              set(['greeting(s)', 'oops(s)']))
store_segment (session, doc, 'Auf Wiedersehen',     set(['goodbye(s)',  'formal(s)']))
store_segment (session, doc, 'Tschüss',             set(['goodbye(s)',  'informal(s)']))

session.commit()

